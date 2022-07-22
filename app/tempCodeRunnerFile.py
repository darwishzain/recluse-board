    with open(tFile,'r') as tCsv:
            tReader = csv.reader(tCsv)
            for row in tReader:
                tValue.append(row)
        for x in range(7):
            for y in range(24):
                Label(dTFrame, justify="left", bg=tValue[x][25], text=tValue[x][y]).grid(row=x, column=y, ipady=5, sticky='nesw')
