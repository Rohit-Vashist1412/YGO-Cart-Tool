import pdfplumber
import pandas as pd
import sys

file_path = sys.argv[1]

# Extract tables using pdfplumber
tables = []
with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        extracted_tables = page.extract_tables()
        for table in extracted_tables:
            tables.append(table)

# We are interested in tables[9] and tables[10] for main and extra decks respectively
main_deck_table = tables[9]
extra_deck_table = tables[10]


monster_cards = {}
spell_cards = {} 
trap_cards = {}
extra_deck = {}
side_deck = {} 

card_dicts = [monster_cards, spell_cards, trap_cards, extra_deck, side_deck]

for row in main_deck_table:
    monster_cards[row[1]] = row[0] 
    
    spell_cards[row[3]] = row[2] 
    
    trap_cards[row[5]] = row[4] 

for row in extra_deck_table:
    extra_deck[row[1]] = row[0] 
    
    side_deck[row[3]] = row[2]


def clean_dict(input_dict):
    # Convert the dictionary to a list of tuples and remove the first and last items
    items = list(input_dict.items())[1:-1]
    
    # Clear the original dictionary
    input_dict.clear()
    
    # Update the original dictionary with filtered items
    input_dict.update({k: v for k, v in items if k and v}) 

#Loop through card dicts to clean them 
for i in range(len(card_dicts)):
    card_dicts[i] = clean_dict(card_dicts[i])


def dict_to_df(card_dict, card_type):
    df = pd.DataFrame(card_dict.items(), columns=['Card Name', 'Quantity'])
    df['Card Type'] = card_type
    return df

# Convert all dictionaries to DataFrames
monster_df = dict_to_df(monster_cards, 'Monster')
spell_df = dict_to_df(spell_cards, 'Spell')
trap_df = dict_to_df(trap_cards, 'Trap')
extra_deck_df = dict_to_df(extra_deck, 'Extra Deck')
side_deck_df = dict_to_df(side_deck, 'Side Deck')

# Combine all DataFrames into one
combined_df = pd.concat([monster_df, spell_df, trap_df, extra_deck_df, side_deck_df])

# Reset the index of the final DataFrame
combined_df.reset_index(drop=True, inplace=True)