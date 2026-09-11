import csv

with open('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv', 'r') as f:
    lines = f.readlines()
    reader = csv.DictReader(lines)
    data = list(reader)
    
# Filter out header rows
data = [row for row in data if row['Venue'] not in ['Topgolf Venue', '{"ImportId":"Venue"}', '']]

# Count venues
venues = {}
for row in data:
    v = row.get('Venue', '').strip()
    if v:
        venues[v] = venues.get(v, 0) + 1

print(f"Venues in file: {venues}")
print(f"Total records: {len(data)}")
