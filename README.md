scripts/add_coordinates.py is useful for combining 
the prevalence data with the metadata so that coordinates are present

scripts/merge_summaries.py can be used to concatenate multiple summaries into one
if there are multiple datasets (e.g. across different years) this should definitely be used
before mapping

prevalence summaries contains the raw data pre-merge and the merged data

app.py should be edited to point to the correct summary file
this can be tested before starting a singularity instance by running 
python app.py in a conda environment with the dependencies installed

setting up the singularity instance when ready
1. Edit the bash script to choose the port you want the server to run on
2. Run the bash script.  It will stop the current singularity instance if it is present and then 
run a new singularity instance (pulling in an image from singularity hub)
3. Visit the hosted website 
