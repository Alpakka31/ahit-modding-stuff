# Set an absolute path to where your game Localization files exist. Use a directory to recurse through all the files like for example: Localization/INT
$LocalizationFilesPath = ""

# Set the path to the localization file cleaner itself.
$LocalizationFileCleanerPath = ""

Foreach ($file in Get-ChildItem -Path $LocalizationFilesPath -Recurse -ErrorAction SilentlyContinue -Force) {
	$fullName = $file.FullName
	$ext = [IO.Path]::GetExtension($fullName)

	# Skip already cleaned files
	if ($ext -eq ".cleaned") {
		continue
	}

	Write-Host "Processing: $fullName"
	& python $LocalizationFileCleanerPath -f "$fullName"
}
