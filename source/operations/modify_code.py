
replacement_dict = {
    'android:debuggable="true"': 'android:debuggable="false"',
    'android:allowBackup="true"': 'android:allowBackup="false"',
    'android:usesCleartextTraffic="true"': 'android:usesCleartextTraffic="false"',
    'android:exported="true"': 'android:exported="false"'
}

def modify_code(filepath):
    with open(filepath, "r+", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        modified_lines = []

        for line in lines:
            modified_line = line
            for search_word, replacement_word in replacement_dict.items():
                if search_word in line:
                    modified_line = modified_line.replace(search_word, replacement_word)

            modified_lines.append(modified_line)

        file.seek(0)
        file.truncate()

        for modified_line in modified_lines:
            file.write(modified_line)