def format_number_ranges(numbers):
    ranges = []
    numbers.sort()
    start = end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = num

    # Add the last range
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ', '.join(ranges)


# takes a list of objects that have team_id and year, and returns it grouped by team_id and with years property
# that is all the years formatted to be more readable
def format_team_years(player_data):
    formatted_teams = {}
    for playing_year in player_data:
        if playing_year['team_id'] not in formatted_teams.keys():
            formatted_teams[playing_year['team_id']] = {'base': playing_year, 'years': [playing_year['year']],
                                                        'players': []}
        else:
            formatted_teams[playing_year['team_id']]['years'].append(playing_year['year'])

    result = []
    for team in formatted_teams.values():
        team['base']['years'] = format_number_ranges(team['years'])
        result.append(team['base'])

    return result
