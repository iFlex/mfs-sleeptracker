# mfs-sleeptracker

Service that pulls fitness data from FitBit and insert it into InfluxDB.

Requirements:
1. External Scheduling
2. EXternal InfluxDB installation + credentials
3. FitBit Application credentials
4. Working_dir folder accessible to user running the application

/working_dir
	/bin/* - location of python and js source scripts
	/config.json - 
	/token.json
	/upload_backlog/[measurement]/year=/month=/day=/hour=/
	/download_backlog/[measurement]/year=/month=/day=/hour=/