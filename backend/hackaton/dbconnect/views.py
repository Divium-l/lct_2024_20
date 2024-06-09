import json
import psycopg2
import subprocess
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dbconnect.models import DatabaseConnection


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

            if db_type != None and db_type.lower() == 'postgreSQL'.lower():
                try:
                    connection = psycopg2.connect(
                        host=url,
                        port=port,
                        user=user,
                        password=password
                    )
                    connection.close()
                    if copy:
                        dump_command = f'pg_dump -h {url} -p {port} -U {user} -F c -b -v -f db_backup.dump'
                        dump_process = subprocess.run(dump_command, shell=True, check=True,
                                                      env={"PGPASSWORD": password})

                        if dump_process.returncode != 0:
                            return JsonResponse({'message': 'Error during database dump'}, status=400)

                        restore_command = f'pg_restore -h {url} -p {port} -U {user} -d new_database -v db_backup.dump'
                        restore_process = subprocess.run(restore_command, shell=True, check=True,
                                                         env={"PGPASSWORD": password})

                        if restore_process.returncode != 0:
                            return JsonResponse({'message': 'Error during database restore'}, status=400)

                        return JsonResponse({'message': 'Connection and copy successful'}, status=200)

                    DatabaseConnection.objects.create(
                            database_type=db_type,
                            url=url,
                            port=port,
                            user=user,
                            password=password,
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

            if db_type == 'postgreSQL':
                try:
                    connection = psycopg2.connect(
                        host=url,
                        port=port,
                        user=user,
                        password=password
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
                    columns_info = {}

                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"""
                            SELECT column_name
                            FROM information_schema.columns
                            WHERE table_name = '{table_name}'
                        """)
                        columns = cursor.fetchall()
                        columns_info[table_name] = {column[0]: False for column in columns}

                        global saved_data
                        saved_data = columns_info

                    connection.close()
                    return JsonResponse(columns_info, status=200)

                except Exception as e:
                    return JsonResponse({'message': str(e)}, status=400)
            else:
                return JsonResponse({'message': 'Unsupported database type'}, status=400)

        except DatabaseConnection.DoesNotExist:
            return JsonResponse({'message': 'No connection data found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def update_columns(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            global saved_data

            for table, columns in data.items():
                if table in saved_data:
                    saved_data[table].update(columns)
                else:
                    saved_data[table] = columns

            return JsonResponse(saved_data, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_saved_columns(request):
    if request.method == 'GET':
        return JsonResponse(saved_data, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=405)