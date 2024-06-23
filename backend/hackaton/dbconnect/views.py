import json
import random
import threading
from datetime import datetime, date, time
import time
import string
import psycopg2
import subprocess

import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dbconnect.models import DatabaseConnection

from ml.model_func import Dataset, Model
from django.conf import settings

from .model_learn import learn_model

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)



def depersonalize_row(row, columns_to_mask, semantic=True):
    depersonalized_row = {}
    for col, val in row.items():
        if col in columns_to_mask:
            depersonalized_row[col] = depersonalize_value(val, semantic)
        else:
            depersonalized_row[col] = val
    return depersonalized_row

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_int(length):
    return random.randint(10**(length-1), 10**length - 1)

def depersonalize_value(value, semantic=True):
    if isinstance(value, str):
        if semantic:
            return generate_random_string(len(value))
        else:
            return generate_random_string(len(value))
    elif isinstance(value, int):
        if semantic:
            return generate_random_int(len(str(value)))
        else:
            return generate_random_int(len(str(value)))
    elif isinstance(value, (datetime, date, time)):
        if semantic:
            return value  # добавить генерацию
        else:
            return value  # добавить генерацию
    else:
        return value

def depersonalize_row(row, columns_to_mask, semantic=True):
    depersonalized_row = {}
    for col, val in row.items():
        if col in columns_to_mask:
            depersonalized_row[col] = depersonalize_value(val, semantic)
        else:
            depersonalized_row[col] = val
    return depersonalized_row

@csrf_exempt
def depersonalize_data(request):
    if request.method == 'GET':
        try:
            if request.body:
                data = json.loads(request.body.decode('utf-8'))
                semantic = data.get("semantic", True)
            else:
                semantic = True

            last_connection = DatabaseConnection.objects.latest('id')
            db_type = last_connection.database_type
            url = last_connection.url
            port = last_connection.port
            user = last_connection.user
            password = last_connection.password

            depersonalized_data = []

            if db_type != None and db_type.lower() == 'postgreSQL'.lower():
                connection = psycopg2.connect(
                    host=url,
                    port=port,
                    user=user,
                    password=password
                )
                cursor = connection.cursor()

                for table in saved_data.get("tables", []):
                    table_name = table["tableName"]
                    columns_to_mask = [col["name"] for col in table["columns"] if col["mask"]]

                    if columns_to_mask:
                        cursor.execute(f"SELECT * FROM {table_name};")
                        rows = cursor.fetchall()
                        colnames = [desc[0] for desc in cursor.description]
                        for row in rows:
                            row_dict = dict(zip(colnames, row))
                            depersonalized_row = depersonalize_row(row_dict, columns_to_mask, semantic)
                            depersonalized_data.append({table_name: depersonalized_row})

                connection.close()

            else:
                return JsonResponse({'message': 'Unsupported database type'}, status=400)

            return JsonResponse({'depersonalized_data': depersonalized_data}, status=200)

        except DatabaseConnection.DoesNotExist:
            return JsonResponse({'message': 'No connection data found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def connect_to_db(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            db_type = data.get('databaseType')
            url = data.get('url')
            port = data.get('port')
            user = data.get('user')
            password = data.get('password')
            copy = data.get('copy')
            dbname = data.get('dbname')

            if db_type != None and db_type.lower() == 'postgreSQL'.lower():
                try:
                    connection = psycopg2.connect(
                        host=url,
                        port=port,
                        user=user,
                        password=password,
                        database=dbname
                    )
                    connection.close()
                    if copy:
                        backup_file = 'db_backup.dump'
                        pg_dump_command = [
                            '/opt/homebrew/bin/pg_dump',
                            '-h', url,
                            '-p', port,
                            '-U', user,
                            '-d', dbname,
                            '-F', 'c',
                            '-b',
                            '-v',
                            '-f', backup_file
                        ]


                        env = {'PGPASSWORD': password}
                        result = subprocess.run(pg_dump_command, env=env, capture_output=True, text=True)

                        if result.returncode != 0:
                            return JsonResponse({'message': f'pg_dump failed: {result.stderr}'}, status=400)

                    DatabaseConnection.objects.create(
                            database_type=db_type,
                            url=url,
                            port=port,
                            user=user,
                            password=password,
                            dbname=dbname,
                            copy=copy
                    )
                    return JsonResponse({'message': 'Connection successful'}, status=200)

                except Exception as e:
                    return JsonResponse({'message': str(e)}, status=400)
                except Exception as e:
                    return JsonResponse({'message': str(e)}, status=400)
            else:
                return JsonResponse({'message': 'Unsupported database type'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def use_saved_connection(request):
    if request.method == 'GET':
        try:
            last_connection = DatabaseConnection.objects.latest('id')
            return JsonResponse({
                'databaseType': last_connection.database_type,
                'url': last_connection.url,
                'port': last_connection.port,
                'user': last_connection.user,
                'password': last_connection.password,
                'dbname':last_connection.dbname,
                'copy': last_connection.copy
            }, status=200)
        except DatabaseConnection.DoesNotExist:
            return JsonResponse({'message': 'No connection data found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_columns(request):
    if request.method == 'GET':
        try:
            last_connection = DatabaseConnection.objects.latest('id')
            db_type = last_connection.database_type
            url = last_connection.url
            port = last_connection.port
            user = last_connection.user
            password = last_connection.password
            dbname = last_connection.dbname

            if db_type.lower() == 'postgreSQL'.lower():
                try:
                    connection = psycopg2.connect(
                        host=url,
                        port=port,
                        user=user,
                        password=password,
                        database=dbname
                    )
                    cursor = connection.cursor()

                    # cursor.execute("SELECT schema_name FROM information_schema.schemata;")
                    cursor.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public';
                    """)
                    tables = cursor.fetchall()
                    print('tables', tables)
                    columns_info = []

                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"""
                            SELECT column_name
                            FROM information_schema.columns
                            WHERE table_name = '{table_name}'
                        """)
                        columns = cursor.fetchall()

                        model_name = r.get("current_model")
                        d = Dataset(last_connection.user, last_connection.password, dbname,  last_connection.url, last_connection.port, table_name)
                        print(str(str(settings.MODELS_PATH)+str(model_name.decode("utf-8"))))
                        m = Model(str(str(settings.MODELS_PATH)+str(model_name.decode("utf-8"))), d)


                        columns_info.append({
                            "tableName": table_name,
                            "columns": [{
                                "name": column[0],
                                "mask": m.get_predictions([column[0]])[column[0]]
                            } for column in columns
                            ]
                        })
                    connection.close()
                    global saved_data
                    saved_data = {"tables": columns_info}
                    return JsonResponse(saved_data, status=200, safe=False)

                except Exception as e:
                    print(repr(e))
                    print(e)
                    return JsonResponse({'message': str(e)}, status=400)
            else:
                return JsonResponse({'message': 'Unsupported database type'}, status=400)

        except DatabaseConnection.DoesNotExist:
            print("NOT FOUND")
            return JsonResponse({'message': 'No connection data found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=405)
@csrf_exempt
def update_columns(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            last_connection = DatabaseConnection.objects.latest('id')
            saved_data = last_connection.saved_data
            if not saved_data:
                saved_data = {}

            for new_table in data.get("tables", []):
                table_name = new_table["tableName"]
                new_columns = new_table["columns"]

                existing_table = next((table for table in saved_data.get("tables", []) if table["tableName"] == table_name), None)

                if existing_table:
                    for new_column in new_columns:
                        column_name = new_column["name"]
                        mask = new_column["mask"]

                        existing_column = next((col for col in existing_table["columns"] if col["name"] == column_name), None)
                        if existing_column:
                            existing_column["mask"] = mask
                        else:
                            existing_table["columns"].append({"name": column_name, "mask": mask})
                else:
                    saved_data.setdefault("tables", []).append({
                        "tableName": table_name,
                        "columns": new_columns
                    })
                    last_connection.saved_data = saved_data
                    last_connection.save()
            return JsonResponse(saved_data, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_saved_columns(request):
    if request.method == 'GET':
        return JsonResponse(saved_data, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def learn(request):
    if request.method == 'GET':
        t = threading.Thread(target=learn_model, daemon=True)
        t.start()
        return JsonResponse({'message': "OK"}, status=200)