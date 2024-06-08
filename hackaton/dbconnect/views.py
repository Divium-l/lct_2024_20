import json
import psycopg2
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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

            if db_type == 'postgreSQL':
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
