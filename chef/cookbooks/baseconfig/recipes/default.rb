# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

# other config 
package "python-dev"
package "python-pip"


package "postgresql-server-dev-all"

execute 'update_pip' do
	command 'pip install --upgrade pip'
end

execute 'pip_install' do
  command 'pip install flask psycopg2 flask-sqlalchemy flask-wtf flask-mail flask-uploads flask-login'
end

#nginx
package "nginx"
cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end

execute "nginx_restart" do
  command 'service nginx restart'
end

#postgres 
package "postgresql"
#creating database
execute 'postgres_user' do
  command 'echo "CREATE DATABASE peer_quiz; CREATE USER ubuntu superuser; GRANT ALL PRIVILEGES ON DATABASE peer_quiz TO ubuntu;" | sudo -u postgres psql'
end

execute 'restart_postgresql' do
  command 'sudo service postgresql restart'
end

#gunicorn
execute 'install_gunicorn' do
  command 'pip install gunicorn'
end

directory "/var/log/gunicorn" do
  owner 'ubuntu'
end

cookbook_file "gunicorn.service" do
    path "/lib/systemd/system/gunicorn.service"
    mode "0644"
    action :create
end
execute "gunicorn-systemd" do
    command "systemctl enable gunicorn"
end
execute "gunicorn" do
    command "systemctl restart gunicorn || systemctl start gunicorn"
end





