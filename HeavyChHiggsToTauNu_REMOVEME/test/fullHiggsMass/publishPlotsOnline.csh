#/bin/csh

###################################################################
#
# This script takes certain graphics files from this folder and
# copies them to ~strichte/public/plots/. There, they are linked
# to in index.html, which places them in a handy table that can be
# viewed online: http://cmsdoc.cern.ch/~strichte/plots/index.html
# (CTRL-click link to view).
#
# Author:       Stefan Richter (strichte)
# Initial edit: 2013-01-29 
#
# Note: As it is, only strichte has the necessary permissions to
#       execute the commands in this script.
#
###################################################################

# Backup previous plots
#TODO: rename them with a name including the current date and time and move them
#into a subdirectory called "old_plots" or similar

# Copy new plots into public folder
cp ./*.png ~strichte/public/html/plots/plot_repository/

# Write update information to log file
#TODO: optional message that can be put into log
#Otherwise just write basic information (time of update)

# Publish date and time of last update (i.e., insert into index.html)
#TODO
