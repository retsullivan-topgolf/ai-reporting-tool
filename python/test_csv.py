import csv

with open('../example-data/topgolf_qualtrics_week_responses.csv', 'r') as f:
    lines = f.readlines()
    print(f"Total lines: {len(lines)}")
    
    # The first line has the actual column names
    # Line 0: StartDate,EndDate,...,Venue,VisitDate,...
    # Line 1: Start Date,End Date,...,Topgolf Venue,Date of Visit,...
    # Line 2: ImportId metadata
    # Line 3+: Data
    
    # Use line 0 as header
    reader = csv.DictReader(lines)
    data = list(reader)
    print(f"\nTotal records: {len(data)}")
    if data:
        print(f"First record keys: {list(data[0].keys())}")
        print(f"First record venue: {data[0].get('Venue')}")
        print(f"First record LTR: {data[0].get('Q1_LTR')}")
        
        # Count venues
        venues = {}
        for row in data:
            v = row.get('Venue', '').strip()
            venues[v] = venues.get(v, 0) + 1
        print(f"\nVenues: {venues}")
