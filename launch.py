def start_vigil():
    print ("""
        

        +-----------------------------------+
            VIGIL 
            real time weapons detection system

            v012.20241023
            Gregory Roberts + John Heilman
        +-----------------------------------+

        """)

    # user input of objects to detect
    searchtext = input("\nType object classes to detect, separated by periods. \n(hit <enter> for default of 'person. face. gun.')\n>>> ")
    if searchtext == "":
        searchtext = "gun. person. face."

    labels = [value.strip() for value in searchtext.split(".")]

    return searchtext, labels