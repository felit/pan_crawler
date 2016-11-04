# config valid only for current version of Capistrano
#lock '3.5.0'

set :application, 'yunpan_crawler'
set :repo_url, '/var/repositories/pan_crawler.git'

# Default branch is :master
# ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, '/var/crawler'

# Default value for :scm is :git
# set :scm, :git

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: 'log/capistrano.log', color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# set :linked_files, fetch(:linked_files, []).push('config/database.yml', 'config/secrets.yml')

# Default value for linked_dirs is []
# set :linked_dirs, fetch(:linked_dirs, []).push('log', 'tmp/pids', 'tmp/cache', 'tmp/sockets', 'public/system')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
# set :keep_releases, 5

namespace :deploy do

  task :published do
    on roles(:app), in: :groups, limit: 3, wait: 10 do
      within(current_path) do
         #execute :python,'accounts_scheduler.py'
         execute "ps -ef | grep accounts | grep -v grep | awk '{print $2}'|xargs kill -9"
         execute :screen, ' -d -m python accounts_scheduler.py'
         execute :python, 'scripts/stats.py'
      end
    end
  end

end
