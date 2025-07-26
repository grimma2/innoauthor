from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Clean up orphaned records from projects_reportproject table'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Check if the table exists
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'projects_reportproject'
                    );
                """)
                
                table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    # Delete orphaned records
                    cursor.execute("""
                        DELETE FROM projects_reportproject 
                        WHERE project_id NOT IN (
                            SELECT id FROM projects_project
                        );
                    """)
                    
                    deleted_count = cursor.rowcount
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully deleted {deleted_count} orphaned records from projects_reportproject'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Table projects_reportproject does not exist')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error cleaning up orphaned records: {str(e)}')
                ) 