# mfs-fitness

Service that reports on fitness data and pulls it from various sources
First implemented source is FitBit
Second source is a manual insert frontend

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