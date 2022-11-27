import pandas
#![](https://img.shields.io/badge/-Missable-informational?style=for-the-badge&color=red) 
#![](https://img.shields.io/badge/-Multipart-informational?style=for-the-badge&color=orange)
#![](https://img.shields.io/badge/-New%20Game+-informational?style=for-the-badge&color=blue)

# main
if __name__ == "__main__":

    # 0 - DEFINE CONSTS
    GUIDE_PATH = "../../innocence-r/toir-guide/csv/toir-guide.csv"
    OUT_PATH = "../../../projects/innocence-r/toir-guide.md"
    TITLE = "# Tales of Innocence R - Side-Quest Guide\n"

    SEPARATOR = "\n---\n"
    MD_ENTRY_TEMPLATE = """
## Side-Quest #{sub} - {english_title}

{missable} {multipart} {new_game}

|![](https://img.shields.io/badge/-Location-informational?style=for-the-badge&color=lightgray) | {english_location}   |
| :--------------------------------------------------------------------------------------- | :------------------ |
| ![](https://img.shields.io/badge/-Timeline-informational?style=for-the-badge&color=lightgray) | {english_period}    |
| ![](https://img.shields.io/badge/-Reward-informational?style=for-the-badge&color=lightgray)   | {english_reward}    |

{english_main_text}

![](toir-guide/sub{sub}_1.png)  
{english_image_text}

{excel_table}
"""

    # 1 - LOAD DATA + MAP COLUMN NAMES TO VARIABLE NAMES (in the template) 
    dataframe = pandas.read_csv(GUIDE_PATH, encoding='utf-8', converters={'Sub' : str})
    rename_map = {
        # from : to
        "Sub"                : "sub",
        "English Title"      : "english_title",
        "Missable"           : "missable",
        "Multipart"          : "multipart",
        "New Game+"          : "new_game",
        "English Location"   : "english_location",
        "English Period"     : "english_period",
        "English Reward"     : "english_reward",
        "English Main Text"  : "english_main_text",
        "English Image Text" : "english_image_text",
        "Excel Table"        : "excel_table"
    }

    # keep only relevant columns + rename then for replacement 
    filtered_dataframe = dataframe[list(rename_map.keys())].rename(columns=rename_map, errors="raise")  # `errors="raise"` will let you know if you try to rename a column that does not exists
    filtered_dataframe = filtered_dataframe.fillna("")
    # 2 - PREPROCESS DATA TO MAKE IT PRETTIER

    ## change nan location, period and reward for None
    repl_filter = lambda s: "None" if s in ["", "-"] else s # https://stackoverflow.com/questions/21608228/conditional-replace-pandas
    filtered_dataframe['english_location'] = filtered_dataframe['english_location'].map(repl_filter)
    filtered_dataframe['english_period'] = filtered_dataframe['english_period'].map(repl_filter)
    filtered_dataframe['english_reward'] = filtered_dataframe['english_reward'].map(repl_filter)

    pretty_df = filtered_dataframe
    # 3 - FOR EACH ROW, GENERATE AN ENTRY
    all_entries = []
    
    for index, row in pretty_df.iterrows():
        if row['english_title'] == "":
            continue # do not print it since theres like no info

        new_entry = MD_ENTRY_TEMPLATE.format(**row) #  funky python woohoo - https://stackoverflow.com/a/30646873 - replace placeholder by corresponding value in row
        all_entries.append(new_entry)

    # 4 - WRITE OUTPUT TO FILE 
    data = TITLE + SEPARATOR.join(all_entries)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(data)

    print("DONE :)")


