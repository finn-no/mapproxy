# This file is part of the MapProxy project.
# Copyright (C) 2010 Omniscale <http://omniscale.de>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from optparse import OptionParser
from mapproxy.seed.config import load_seed_tasks_conf
from mapproxy.seed.seeder import seed_tasks
from mapproxy.seed.util import format_task


def main():
    usage = "usage: %prog [options] seed_conf"
    parser = OptionParser(usage)
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-s", "--seed-conf",
                      dest="seed_file", default=None,
                      help="seed configuration")
    parser.add_option("-f", "--proxy-conf",
                      dest="conf_file", default=None,
                      help="proxy configuration")
    parser.add_option("-c", "--concurrency", type="int",
                      dest="concurrency", default=2,
                      help="number of parallel seed processes")
    parser.add_option("-n", "--dry-run",
                      action="store_true", dest="dry_run", default=False,
                      help="do not seed, just print output")    
    parser.add_option("-l", "--skip-geoms-for-last-levels",
                      type="int", dest="geom_levels", default=0,
                      metavar="N",
                      help="do not check for intersections between tiles"
                           " and seed geometries on the last N levels")
    parser.add_option("--summary",
                      action="store_true", dest="summary", default=False,
                      help="print summary with all seeding tasks and exit."
                           " does not seed anything.")
    parser.add_option("-i", "--interactive",
                      action="store_true", dest="interactive", default=False,
                      help="print each task decription and ask if it should be seeded")
    
    (options, args) = parser.parse_args()
    if not options.seed_file:
        if len(args) != 1:
            parser.error('missing seed_conf file as last argument or --seed-conf option')
        else:
            options.seed_file = args[0]
    
    if not options.conf_file:
        parser.error('missing mapproxy configuration -f/--proxy-conf')
    
    tasks = load_seed_tasks_conf(options.seed_file, options.conf_file)
    
    if options.summary:
        for task in tasks:
            print format_task(task)
        return
    
    if options.interactive:
        selected_tasks = []
        for task in tasks:
            print format_task(task)
            resp = raw_input('seed this (y/n)?')
            if resp.lower() == 'y':
                selected_tasks.append(task)
        
        if selected_tasks:
            print 'start seeding process'
            seed_tasks(selected_tasks, verbose=options.verbose, dry_run=options.dry_run,
                       concurrency=options.concurrency,
                       skip_geoms_for_last_levels=options.geom_levels)
            
    else:
        seed_tasks(tasks, verbose=options.verbose, dry_run=options.dry_run,
                   concurrency=options.concurrency,
                   skip_geoms_for_last_levels=options.geom_levels)
    



if __name__ == '__main__':
    main()
