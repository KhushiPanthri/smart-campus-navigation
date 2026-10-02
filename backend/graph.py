graph = {
    "Main Gate": [
        ("Admin Block", 100),
        ("B-tech Block", 100),
        ("B-tech Tuckshop",50),
        ("Convocation Centre",10),
        ("Gate 3",20),
    ],

    "Admin Block": [
        ("Main Gate", 100),
        ("Main Ground",30),
        ("B-tech Block",0),
        ("Santoshanand Library",30),
        ("Aryabhatta Lab", 40),
        ("Civil Block",50),
        ("Badminton Court",55),
        ("Happiness Cafe",30),
        ("B-tech Tuckshop",50)
    ],
    "B-tech Block": [
        ("Main Gate", 100),
        ("Main Ground",30),
        ("Admin Block",0),
        ("Santoshanand Library",30),
        ("Aryabhatta Lab", 40),
        ("Civil Block",50),
        ("Badminton Court",55),
        ("Happiness Cafe",30),
        ("B-tech Tuckshop",50)       
    ],
    "Santoshanand Library": [
        ("Admin Block", 30),
        ("B-tech Block",30),
        ("Badminton Court",30),
        ("Electrical Block",30),
        ("Aryabhatta Lab",20),
        ("Param Lab",10)
    ],

    "Gate 2": [
        ("Chanakya Block", 45),
        ("KP Nautiyal Block",45),
        ("Chanakya Tuckshop",40),
        ("Convocation Centre",240)
    ],
    "Gate 3": [
        ("CSIT Block", 10),
        ("CSIT Tuckshop",30),
        ("Paramedical Block",30)

    ],

    "CSIT Tuckshop": [
        ("CSIT Block", 10),
        ("Gate 3",10),
        ("Paramedical Block",10)
    ],

    "Chanakya Tuckshop": [
        ("Chanakya Block",5),
        ("KP Nautiyal Block",5),
        ("Gate 2",40)
    ],

    "B-tech Tuckshop": [
        ("B-tech Block",50 ),
        ("Admin Block",50),
        ("Main Gate",50)
    ],

    "Ravi Canteen": [
        ("Happiness Cafe",10 ),
        ("B-tech Block",40),
        ("Admin Block",40,),
        ("CSIT Block",150),
        ("Main Ground",10)
    ],

    "CSIT Block": [
        ("Ravi Canteen",150),
        ("Main Ground",50),
        ("Gate 3",10),
        ("CSIT Tuckshop",10),
        ("Paramedical Block",10),
    ],

    "Chanakya Block": [
        ("Chanakya Tuckshop",5),
        ("KP Nautiyal Block",0)
    ],

    "KP Nautiyal Block": [
        ("Chanakya Block",0),
        ("Chanakya Tuckshop",5)
    ],

    "Old MCA Block": [
        ("Param Lab",20),
        ("Quick Bite Cafe",10),
        ("Mechanical Block",20)
    ],

    "Mechanical Block": [
        ("Old MCA Block",20),
        ("Aryabhatta Lab",10)
    ],

    "Civil Block": [
        ("Badminton Court",5),
        ("Basketball Court",10)
    ],

    "Electrical Block": [
        ("Basketball Court",5),
        ("Santoshanand Library",30),
        ("Param Lab",35)
    ],

    "Paramedical Block": [
        ("CSIT Block",10),
        ("CSIT Tuckshop",5)
    ],

    "Convocation Centre": [
        ("Main Gate", 10),
        ("Gate 2",240)
    ],

    "Aryabhatta Lab": [
        ("Mechanical Block",10),
        ("Santoshanand Library",20)
    ],

    "Param Lab": [
        ("Santoshanand Library",10),
        ("Old MCA Block",20)
    ],

    "Happiness Cafe": [
        ("Ravi Canteen",10),
        ("B-tech Block",30),
        ("Admin Block",30,),
        ("Badminton Court",55),
        ("Civil Block",50)
    ],

    "Quick Bite Cafe": [
        ("KP Nautiyal Block",20),
        ("Chanakya Block",20),
        ("Old MCA Block",10)
    ],

    "Main Ground": [
        ("CSIT Block",50),
        ("B-tech Block",30),
        ("Admin Block",30,),
        ("Ravi Canteen",10)
    ],

    "Basketball Court": [
        ("Civil Block", 10),
        ("Electrical Block",5)
    ],

    "Badminton Court": [
        ("Civil Block",5),
        ("B-tech Block",55)
    ]
}

