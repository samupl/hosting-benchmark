import os
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import click


@click.command(help='Create an archive with the PHP code')
@click.option(
    '--skip-credentials',
    default=False,
    is_flag=True,
    help='Do not create config.php file with DB credentials'
)
@click.option(
    '--db-host',
    default='',
    help='MySQL database hostname',
)
@click.option(
    '--db-user',
    default='',
    help='MySQL database username',
)
@click.option(
    '--db-pass',
    default='',
    help='MySQL database password',
)
@click.option(
    '--db-name',
    default='',
    help='MySQL database name',
)
def main(db_host, db_user, db_pass, db_name, skip_credentials):
    if not skip_credentials and not db_host:
        db_host = click.prompt('Database hostname')
    if not skip_credentials and not db_name:
        db_name = click.prompt('Database name')
    if not skip_credentials and not db_user:
        db_user = click.prompt('Database username')
    if not skip_credentials and not db_pass:
        db_pass = click.prompt('Database password', hide_input=True)

    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_dir = os.path.join(pkg_dir, 'server')
    target_path = os.path.join(os.getcwd(), 'hosting_benchmark.zip')

    with ZipFile(target_path, 'w') as zip_file:
        for folder_name, subfolders, filenames in os.walk(server_dir):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_file.write(
                    filename=file_path,
                    arcname=file_path.replace(server_dir, '')
                )

        if not skip_credentials:
            with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
                tmp_file.write('<?php\n')
                tmp_file.write(f'$dbhost = "{db_host}";\n')
                tmp_file.write(f'$dbpass = "{db_pass}";\n')
                tmp_file.write(f'$dbuser = "{db_user}";\n')
                tmp_file.write(f'$dbname = "{db_name}";\n')

                tmp_file.seek(0)

                zip_file.write(
                    filename=tmp_file.name,
                    arcname=tmp_file.name.replace(tmp_file.name, 'config.php')
                )

    click.echo(
        f'An archive with the server PHP code has been created: {target_path}'
    )
