import json

filename = 'population_data.json'
with open(filename) as f:
    pop_data = json.load(f)
for pop_dict in pop_data:
    print(pop_dict)
    if pop_dict['Year'] == '1960':
        country_name = pop_dict['Country Name']
        population = pop_dict['Value']
        print(country_name + ':' + population)
