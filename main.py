import PySimpleGUI as sg
import requests
import cosine

sg.theme('Reddit')   # Add a touch of color
# All the stuff inside your window.
query_column = [
        # left column
        [sg.Text('Write your movie description here:')],
        [sg.Multiline(key="query", size=(30,10))],
        [sg.Radio('cosine', "Radio1", key='cosine', default=True)],
        [sg.Radio('Solr', "Radio1", key='solr', default=False)],
        # [sg.HSeparator()],
        # [sg.Checkbox('Include ratings', key='ratings', default=False)]
    ]
results_column = [
        # right column
        [sg.Text("Results", size=(30,1))],
        [sg.Text("", key='result_list')]
    ]
layout = [
    [sg.Text('Movie Plot Search')],
    [
        sg.Column(query_column, vertical_alignment='t'),
        sg.VSeparator(),
        sg.Column(results_column, vertical_alignment='t'),
    ],
    [sg.Button('Search'), sg.Button('Exit')]
]

# Create the Window
window = sg.Window('Movie Plot Search', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    # print(event)
    if event == 'Search':
        # print('You entered:\n', values['query'], '\n')
        query = values['query']
        useCosine = values['cosine']
        # useRatings = values['ratings']
        keywords = query.replace(" ", "%2C")
        # print(keywords)
        result_list = ""

        if useCosine:
            result = cosine.movie_similarities(query)
            titles = list(result["Title"])
            years = list(result["Year"])
            score = list(result["Cosine"])
            for i in range(len(titles)):
                result_list += str(i+1) + ". " + titles[i] + " [" + str(years[i]) + "] (" + str(score[i]) + ")\n"
        else:
            url = "http://localhost:8983/solr/movieRatings/select?fl=*%2Cscore&indent=true&q.op=OR&q=Plot%3A" + \
                  keywords + "&rows=10&useParams="
            # print(url)
            result = requests.get(url=url).json()
            # print(result)
            movies = result['response']['docs']
            for i in range(min(10, result['response']['numFound'])):
                title = movies[i]['Title'][0]
                year = str(movies[i]['Release_Year'][0])
                score = str(movies[i]['score'])
                result_list += str(i+1) + ". " + title + " [" + year + "] (" + score + ")\n"

        window['result_list'].update(result_list)


window.close()