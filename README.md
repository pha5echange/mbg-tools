# MBG-Tools alpha v. 0.4

by J. M. Gagen
jmg*AT*phasechange*DOT*info
j*DOT*gagen*AT*gold*DOT*ac*DOT*uk

www*DOT*phasechange*DOT*info

November 8th 2017

These scripts have been created to facilitate research into musical genre using MusicBrainz. 
They acquire raw XML data, and process it.
This is then used by ENG-Tools (in a separate repository).   

This is research software; USE IT AT YOUR OWN RISK. 
I will respond to emails if possible, BUT THIS SOFTWARE HAS NO FORMAL SUPPORT.

LICENCE: 
http://creativecommons.org/licenses/by-nc-sa/3.0/

Tools for the acquisition and processing of MusicBrainz artist data. 

Requires Python 2.7, the 'requests' library, and the 'matplotlib' library. 

The files 'data/en_mb_map.txt' , 'data/artist_list.txt' and 'data/user_tag_list.txt' must be present. 
These contain (in order): a list of MusicBrainz artist IDs, generated from the Echo Nest (see the 'eng-tools' repository); 
a list of artists whose tags will be checked by 'mbg_process_tags': a list of user-tags which are related to genre (manually edited from the full list). 

- 'mb_timeslicer' generates time-limited genre lists (variant of eng-repo 'timeslicer')

- 'mb_cluster' finds clusters of artists within genres (variant of 'eng_cluster.py'). Writes 'data/first_cluster.txt'

- 'mbg_merge_genres' uses 'data/mbg_alternates.txt' to merge genres with their alternates (genres that are the same, other than in name). 

- 'mbg_process_tags' checks artist tags against the list of genre-related user-generated tags, fixes start dates, and generates a folder of genre-based artist lists.  

- 'mbg_get_artists_url' fetches artists from MusicBrainz based on IDs in the Echo Nest map-file

- 'mbg_recording-rels_xml' fetches artists with RECORDING-RELS info

- 'mbg_process_xml' deals with the data, and creates a result files for use by ENG Tools (`eng_mbDate')

- 'mbg_plot_countries' allows manual (hardcoded) plotting of country data