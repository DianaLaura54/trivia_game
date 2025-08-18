import sqlite3
import random

def insert_qa_data():

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    qa_data = {
        'informatics': [
            ('What does CPU stand for?', 'Central Processing Unit', ['Computer Processing Unit', 'Central Processing Unit', 'Central Program Unit', 'Core Processing Unit']),
            ('What does RAM stand for?', 'Random Access Memory', ['Random Access Memory', 'Read Access Memory', 'Rapid Access Memory', 'Ready Access Memory']),
            ('What is the full form of HTML?', 'HyperText Markup Language', ['HyperText Machine Language', 'HyperText Markup Language', 'Hypertext Markup Language', 'HighText Markup Language']),
            ('What does URL stand for?', 'Uniform Resource Locator', ['Uniform Resource Locator', 'Uniform Request Locator', 'Universal Resource Locator', 'Universal Request Locator']),
            ('What is the main function of an operating system?', 'To manage hardware and software resources', ['To provide software tools', 'To manage hardware and software resources', 'To protect the system from malware', 'To store data in memory']),
            ('What does HTTP stand for?', 'HyperText Transfer Protocol', ['HyperText Transfer Protocol', 'HyperText Text Protocol', 'Hyper Transfer Text Protocol', 'High Transfer Text Protocol']),
            ('What is the most common programming language?', 'JavaScript', ['Java', 'Python', 'JavaScript', 'C++']),
            ('What does VPN stand for?', 'Virtual Private Network', ['Virtual Private Network', 'Virtual Public Network', 'Variable Private Network', 'Vocal Private Network']),
            ('What is the function of a router?', 'To forward data packets between networks', ['To forward data packets between networks', 'To process data', 'To store data', 'To secure the system']),
            ('What is the largest social media platform?', 'Facebook', ['Instagram', 'Facebook', 'Twitter', 'Snapchat'])
        ],
        'mathematics': [
            ('What is 2 + 2?', '4', ['3', '4', '5', '6']),
            ('What is the square root of 16?', '4', ['2', '3', '4', '5']),
            ('What is 5 x 5?', '25', ['20', '25', '30', '35']),
            ('What is 7 + 8?', '15', ['12', '13', '15', '16']),
            ('What is 10 divided by 2?', '5', ['4', '5', '6', '7']),
            ('What is the value of pi?', '3.14159', ['3.14', '3.14159', '3.12', '3.16']),
            ('What is the formula for the area of a circle?', 'πr²', ['πr²', 'πd²', 'r²π', '2πr']),
            ('What is 3 squared?', '9', ['6', '8', '9', '12']),
            ('What is 15% of 200?', '30', ['20', '25', '30', '35']),
            ('What is the perimeter of a square with side 5?', '20', ['15', '20', '25', '30'])
        ],
        'physics': [
            ('What is the speed of light?', '299,792,458 m/s', ['299,792,458 m/s', '300,000,000 m/s', '150,000,000 m/s', '500,000,000 m/s']),
            ('What is the force of gravity on Earth?', '9.8 m/s²', ['10 m/s²', '9.8 m/s²', '8.9 m/s²', '9.0 m/s²']),
            ('What is the unit of electric current?', 'Ampere', ['Volt', 'Ohm', 'Ampere', 'Joule']),
            ('What is the boiling point of water in Celsius?', '100', ['90', '100', '110', '120']),
            ('What is the unit of power?', 'Watt', ['Joule', 'Newton', 'Watt', 'Volt']),
            ('What is the first law of thermodynamics?', 'Energy cannot be created or destroyed', ['Energy cannot be created or destroyed', 'Energy increases over time', 'Energy is always conserved', 'Energy can be destroyed']),
            ('What is the unit of force?', 'Newton', ['Joule', 'Newton', 'Meter', 'Watt']),
            ('What is the symbol for velocity?', 'v', ['v', 'u', 'a', 'g']),
            ('What is the energy formula for kinetic energy?', '1/2mv²', ['mgh', '1/2mv²', 'mv', 'mgh²']),
            ('What is the unit of frequency?', 'Hertz', ['Hertz', 'Joule', 'Meter', 'Watt'])
        ],
        'biology': [
            ('What is the powerhouse of the cell?', 'Mitochondria', ['Nucleus', 'Mitochondria', 'Ribosome', 'Endoplasmic Reticulum']),
            ('What is the genetic material of an organism?', 'DNA', ['RNA', 'DNA', 'Protein', 'Chromosome']),
            ('What is the process by which plants make their food?', 'Photosynthesis', ['Respiration', 'Fermentation', 'Photosynthesis', 'Digestion']),
            ('How many chromosomes do humans have?', '46', ['44', '46', '48', '50']),
            ('What is the largest organ in the human body?', 'Skin', ['Heart', 'Liver', 'Lungs', 'Skin']),
            ('What is the chemical symbol for water?', 'H2O', ['H2O', 'CO2', 'O2', 'CH4']),
            ('What do red blood cells carry?', 'Oxygen', ['Oxygen', 'Carbon Dioxide', 'Nutrients', 'Waste']),
            ('What is the process of cell division called?', 'Mitosis', ['Meiosis', 'Mitosis', 'Binary Fission', 'Cytokinesis']),
            ('What is the main function of white blood cells?', 'Fight infection', ['Fight infection', 'Transport oxygen', 'Carry nutrients', 'Regulate hormones']),
            ('What is the function of the nervous system?', 'Transmit signals', ['Transmit signals', 'Digest food', 'Regulate temperature', 'Pump blood'])
        ],
        'chemistry': [
            ('What is the atomic number of Hydrogen?', '1', ['1', '2', '3', '4']),
            ('What is the chemical formula for methane?', 'CH4', ['C2H6', 'CH4', 'C2H4', 'CH3OH']),
            ('What is the pH of pure water?', '7', ['5', '6', '7', '8']),
            ('What is the chemical symbol for gold?', 'Au', ['Ag', 'Au', 'Pb', 'Fe']),
            ('What is the unit of measurement for pressure?', 'Pascal', ['Bar', 'Pascal', 'Pound', 'Newton']),
            ('What is the process of a solid turning into a gas?', 'Sublimation', ['Condensation', 'Sublimation', 'Evaporation', 'Freezing']),
            ('What is the most abundant gas in the Earth\'s atmosphere?', 'Nitrogen', ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Hydrogen']),
            ('What is the formula for carbon dioxide?', 'CO2', ['CO2', 'O2', 'CH4', 'C2H6']),
            ('What is the process by which plants absorb sunlight?', 'Photosynthesis', ['Respiration', 'Photosynthesis', 'Oxidation', 'Reduction']),
            ('What is the atomic number of Carbon?', '6', ['4', '5', '6', '7'])
        ],
        'general': [
            ('Who is known as the father of physics?', 'Isaac Newton', ['Albert Einstein', 'Isaac Newton', 'Nikola Tesla', 'Galileo']),
            ('Which planet is known as the Red Planet?', 'Mars', ['Venus', 'Earth', 'Mars', 'Jupiter']),
            ('What is the capital of France?', 'Paris', ['London', 'Berlin', 'Paris', 'Rome']),
            ('Who wrote the play "Romeo and Juliet"?', 'William Shakespeare', ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'George Orwell']),
            ('What is the largest continent on Earth?', 'Asia', ['Africa', 'Asia', 'Europe', 'Australia']),
            ('Which ocean is the largest?', 'Pacific Ocean', ['Atlantic Ocean', 'Pacific Ocean', 'Indian Ocean', 'Arctic Ocean']),
            ('How many continents are there?', '7', ['6', '7', '8', '9']),
            ('What is the hardest natural substance on Earth?', 'Diamond', ['Gold', 'Iron', 'Diamond', 'Platinum']),
            ('Who painted the Mona Lisa?', 'Leonardo da Vinci', ['Pablo Picasso', 'Leonardo da Vinci', 'Vincent van Gogh', 'Claude Monet']),
            ('Which gas do plants absorb during photosynthesis?', 'Carbon Dioxide', ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'])
        ]
    }

    question_id = 1
    set_id = 1

    for category, questions in qa_data.items():
        for question, correct_answer, options in questions:
            random.shuffle(options)


            cursor.execute('''
                    INSERT INTO question (idint, question, var1, var2, var3, var4, correct)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                question_id,
                question,
                options[0],
                options[1],
                options[2],
                options[3],
                correct_answer
            ))


            cursor.execute('''
                    INSERT INTO test (idset, idint)
                    VALUES (?, ?)
                ''', (
                set_id,
                question_id
            ))

            question_id += 1

        set_id += 1

    conn.commit()
    conn.close()


insert_qa_data()