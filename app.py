import os
import uuid
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from deep_translator import GoogleTranslator
import google.generativeai as genai


# Configuration
class Config:
    UPLOAD_FOLDER = "static"
    GEMINI_API_KEY = "AIzaSyAYCE9RjUhr4YtzM5XDr66zZYdKgojhz7Q"  # Move to environment variables
    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = True


# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

# Initialize Gemini AI
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# College data repository
COLLEGE_DATA = {
    "about": "Godavari Institute of Engineering and Technology (GIET), established in 1998, is known for academic excellence and innovation.",

    "courses": "Undergraduate: CSE, ECE, EEE, ME, Civil, AI & ML, DS, Cyber Security. Postgraduate: M.Tech in CSE, VLSI, Power Systems, MBA, MCA.",

    "departments": "CSE, ECE, EEE, IT, ME, Civil, AI & DS, AI & ML, MBA, MCA.",

    "admission": "B.Tech via AP EAMCET/JEE Main, M.Tech via GATE/PGECET, MBA/MCA via ICET.",

    "fees": "Approx ₹80,000 – ₹1,50,000/year for BTech. Scholarships available.",

    "contact": "Phone: 0883-2484825, +91 99499 93483 | Email: info@giet.ac.in | Website: www.giet.ac.in",

    "location": "NH-16, Chaitanya Knowledge City, Rajahmundry, Andhra Pradesh – 533296.",

    "facilities": "Hostels (AC & Non-AC), Wi-Fi campus, Library, Cafeteria, Medical, Gym, Transport, Sports Complex.",

    "hostel": "Separate boys and girls hostels with mess and security.",

    "placement": "Highest package: 35 LPA. Avg: 4.5 LPA. Recruiters: Microsoft, Amazon, TCS, Infosys, Wipro, etc.",

    "accreditation": "NAAC A++ (Cycle 2), NBA accredited depts, AICTE/ISO certified, NIRF rank 201–250.",

    "bus": "Bus facility available for students and staff from various towns.",

    "university": "GIET is now a university named Godavari Global University (GGU) – ggu.edu.in, AP EAPCET code: GGURPU.",

    "programs": "Programs: Engineering, Pharmacy, MBA, MCA, BSc, BCA, BPT, Diploma, PhD across various schools.",

    "events": "Campus events include Medha, Maitri, tech fests, workshops, and NSS programs.",

    "clubs": "Technical clubs, Cultural clubs, Entrepreneurship Cell,NCC,IOT club,hlo world,Digital Marketing club,Visual vortex,Robo club.",

    "centers": "Centers of Excellence by Apple, Oracle, Red Hat.",

    "faculty": "200+ faculty, 48 with PhDs.",

    "students": "10,000+ students, 20,000+ alumni.",

    "campus_area": "300-acre lush green campus.",

    "technical_hubs": "GIET TechWing is a training initiative by GIET University focused on providing students with industry-relevant technical and professional skills, TechWing offers training in various in-demand areas like advanced coding, Gen AI & AWS, UI&UX, RED HAT, and full-stack development, Java",

    "canteens": "Food courts available: Central Food Court, Yummips. Items include Biryani, Fried Rice, Noodles, Parota, Pizza, Manchuria, Burgers, Ice Creams, Maggie, etc.",

    "library": """Books in the library:
1. EEE: 4764
2. ECE: 5010
3. MECH: 5013
4. CSE: 4758
5. IT: 3256
6. CIVIL: 2012
7. MINING: 1768
8. AUTOMOBILE: 1759
9. M.Tech - Power Systems: 1207
10. Software Engg: 1215
11. VLSI & Embedded: 405
12. MBA: 6527
13. MCA: 10513""",

    "beautiful_locations": """Beautiful Campus Spots:
• Bamboos Way
• Amphitheatre
• Lakeview""",

    "grounds": "Playgrounds available on campus include a basketball ground, volleyball ground, cricket ground, football ground, and two spacious bus grounds suitable for large events and sports activities.",

    "degree_courses": "B.ScMathematics, Physics, Chemistry, B.ScMathematics, Physics, Computer Science, B.ScMathematics, Statistics, Computer Science, B.ScForensic Science, B.ScAnimation, BCABachelor of Computer Applications, B.ComComputer Applications, BBAGeneral, BBADigital Marketing.",

    "hostel_mess": "very bad and worst when compared to home food, only curd is very delicious, 40+ rooms, girls and boys are seperated, morning-7-9am, afternoon-12-2pm, evening-5-6pm, night-7:30-9pm",

    "telugu_maha_sabhalu": "telugu maha sabhalu is the second international telugu conference was held from 5 to 7 january 2024 and 10 to 12 january 2025 in giet",
    "degree courses": "B.ScMathematics, Physics, Chemistry,B.ScMathematics, Physics, Computer Science,B.ScMathematics, Statistics, Computer Science,B.ScForensic Science,B.ScAnimation,BCABachelor of Computer Applications,B.ComComputer Applications,BBAGeneral,BBADigital Marketing.",
    "boarding Points":" Bus routes are available for these routes Diwancheruvu,,Penuguru,Jangareddy gudem,Rajahmundry,Rajanagaram,Peddapuram,Surampalem,Kakinada,Pitapuram,Anaparthi,Dwarapudi,Kovvuru,Madiki,Dowleswaram,Kadiyam,Vemagiri,Bommuru,Kadiyapulanka,Ravulapalem,Edidha,Mandapeta,Kesavaram.....  for further details contact transport department",
    "blocks":"Main block,VB block ,Rk block ,Polytechnic Block,Pharmacy block ,Degree block ,Giet 2nd campus",
    "university":
    """name: Godavari Global University,
    abbreviation: GGU,
    status: GIET IS NOW UNIVERSITY,
    website: ggu.edu.in,
    phone: 994 999 3483,
    history: With 26 years history of excellence as GIET - Autonomous, the institution’s transformation into Godavari Global University underscores its stability, credibility and dedication to academic excellence""",
    "hospital":"Medunit clinic is available for any emergency treatment in the college and medicines are available ",
    "gym":"no gym in our college",
    "course fee":"""
1. EEE: 1,00,000
2. ECE: 1,50,000
3. MECH: 90,000
4. CSE: 1,75,000
5. IT: 1,00,000
6. CIVIL: 90,000
7. MINING: 80,000
8. AUTOMOBILE: 85,000
9. M.Tech - Power Systems: 80,000
10. Software Engg: 89,000
11. VLSI & Embedded: 90,000
12. MBA: 2,70,000
13. MCA: 2,00,000
14.AIML - 1,30,000
15.Data Science:1,25,000
16.Bus fee:25,000""",
"cutoffs": """
GIET Engineering College, Rajahmundry (AP EAMCET):
1. B.Tech Computer Science and Engineering
   - 2024: Closing rank 21645
   - 2023: Closing rank 34806
2. B.Tech Electronics and Communication Engineering
   - 2024: Closing rank 30735
   - 2023: Closing rank 27730
3. B.Tech Information Technology
   - 2024: Closing rank 46786
   - 2023: Closing rank 50879
4. B.Tech Mechanical Engineering
   - 2024: Closing rank 82974
   - 2023: Closing rank 103838
5. B.Tech Artificial Intelligence and Machine Learning
   - 2024: Closing rank 42106
6. B.Tech Data Science
   - 2024: Closing rank 49177

GIET General (Other AP EAPCET Streams):
1. B.Tech Mechanical Engineering
   - 2024: Closing rank 143436
   - 2023: Closing rank 147833
2. B.Tech Civil Engineering
   - 2024: Closing rank 143896
   - 2023: Closing rank 143400
3. B.Tech Agricultural Engineering
   - 2024: Closing rank 150359
4. B.Tech Electrical and Electronics Engineering
   - 2024: Closing rank 129995
   - 2023: Closing rank 132921

GIET School of Pharmacy:
- Admission through AP EAPCET counseling.
- Visit official website for application form.

""",
    "juice shop":"available all juices may include Mango,pineapple,Badham,Dry fuits ,Ice creams,Grapes,Musk Melon,Apple,Banana,Lassi,Blue berry,Strawberry etc",
    "Zerox":"Zerox shop is available in the college can take zerox of files,records and icludes books and pens all necessary sanitary items",
    "distance":"""
1.Rk block:700 meters from main campus
2.Polytechnique block:720 meters from main block and 20 meters from rk block
3.Pharmacy block: 650 meters from main campus and 50 meetrs from rk block
4.Giet2:2000 meters from main campus 
5.Degree block :250 meters  from giet2 campus and 2250 meters from main campus
6.Zerox shop:30 meters distance from main campus
7.Food court:80 meters from main campus
8.Juice shop:20 meters from main campus
9.Yumpies: 200 meters from main campus
10.Girls hostel: 500 meters from main campus
11.Boys hostel: 450  meters from main campus
12.Mess: 230 meters from main campus
13.central food court: 340 meters from main campus
""",





}




# Keywords for topic matching
TOPIC_KEYWORDS = {
    "about": ["introduction", "overview", "history", "established", "founded"],
    "courses": ["course", "courses", "program", "programs", "branch", "branches", "btech", "b.tech", "mtech", "m.tech",
                "mba", "mca", "degree", "degrees", "stream", "streams", "study", "studies"],
    "departments": ["department", "departments", "faculty", "faculties", "school", "schools"],
    "admission": ["admission", "admissions", "join", "joining", "entrance", "apply", "application", "eligibility",
                  "qualify", "enroll", "enrollment"],
    "fees": ["fee", "fees", "cost", "costs", "tuition", "expenses", "charges", "payment", "scholarship",
             "scholarships"],
    "contact": ["contact", "phone", "call", "email", "website", "reach", "connect"],
    "location": ["location", "where", "address", "city", "place", "situated", "located"],
    "facilities": ["facility", "facilities", "infrastructure", "amenities", "services"],
    "hostel": ["hostel", "hostels", "accommodation", "stay", "room", "rooms", "residence", "boarding"],
    "placement": ["placement", "placements", "job", "jobs", "recruiter", "recruiters", "package", "packages", "company",
                  "companies", "career", "careers", "employment"],
    "accreditation": ["accreditation", "accredited", "naac", "nba", "aicte", "iso", "nirf", "ranking", "rank",
                      "recognition", "certified"],
    "bus": ["bus", "buses", "transport", "transportation", "travel", "commute"],
    "university": ["university", "ggu", "global university", "godavari global"],
    "programs": ["bsc", "b.sc", "bca", "b.ca", "bpt", "b.pt", "msc", "m.sc", "phd", "ph.d", "diploma", "undergraduate",
                 "postgraduate"],
    "events": ["event", "events", "fest", "fests", "festival", "festivals", "workshop", "workshops", "activity",
               "activities", "celebration", "celebrations", "medha", "maitri"],
    "clubs": ["club", "clubs", "cultural", "technical", "e-cell", "entrepreneurship", "society", "societies"],
    "centers": ["center", "centers", "centre", "centres", "excellence", "apple", "oracle", "redhat", "red hat"],
    "faculty": ["teacher", "teachers", "professor", "professors", "staff", "instructor", "instructors"],
    "students": ["student", "students", "alumni", "strength", "population", "enrollment"],
    "campus_area": ["area", "campus", "acres", "land", "size", "space"],
    "technical_hubs": ["technical hubs", "techwing", "professional training", "certifications", "certification courses",
                       "softskills training", "multinational companies", "IIT", "IIM", "global universities",
                       "tech courses", "technical courses"],
    "canteens": ["food courts", "central food court", "food", "canteens", "food items"],
    "library": ["library", "book volumes", "books", "volumes", "CSE volumes", "EEE volumes", "MECH volumes",
                "ECE volumes", "MINING volumes", "CIVIL volumes", "IT volumes", "M.TECH volumes", "AUTOMOBILE volumes",
                "MBA volumes", "MCA volumes", "CSE books", "EEE books", "MECH books", "ECE books", "MINING books",
                "CIVIL books", "IT books", "M.TECH books", "AUTOMOBILE books", "MBA books", "MCA books"],
    "grounds": ["grounds", "playgrounds", "basket ball ground", "valley ball ground", "football ground", "bus ground"],
    "beautiful_locations": ["beautiful", "locations", "bamboos", "amphitheatre", "lakeview", "lake", "photo spots",
                            "nature view", "scenic spots", "greenery", "scenery"],
    "degree_courses": ["bsc", "b.sc", "bca", "b.com", "bba", "undergraduate degree", "degree", "degrees", "ug courses",
                       "bachelor of science", "bachelor of computer applications", "computer applications",
                       "digital marketing", "bba courses", "bsc combinations", "bsc forensic", "bsc animation",
                       "non-engineering programs", "science courses", "bachelor courses", "bachelor programs",
                       "bsc maths", "bsc physics", "bsc chemistry", "bsc cs", "bsc statistics"],
    "hostel_mess": ["hostel mess", "bad food", "worst food", "home food", "curd", "delicious curd", "rooms",
                    "40+ rooms", "separate girls and boys", "boys hostel", "girls hostel", "mess timings",
                    "mess schedule", "morning food", "afternoon food", "evening snacks", "night dinner"],
    "telugu_maha_sabhalu": ["telugu maha sabhalu", "telugu conference", "international telugu conference",
                            "second international", "telugu", "maha sabhalu", "conference in giet", "giet", "2024",
                            "2025", "January 5 to 7", "January 10 to 12"],
    "block":["Main block,VB block ,Rk block ,Polytechnic Block,Pharmacy block ,Degree block ,Giet 2nd campus"],
    "degree_courses":[
    "bsc", "b.sc", "bca", "b.com", "bba", "undergraduate degree", "degree", "degrees", "ug courses",
    "bachelor of science", "bachelor of computer applications", "computer applications", "digital marketing",
    "bba courses", "bsc combinations", "bsc forensic", "bsc animation", "non-engineering programs", "science courses",
    "bachelor courses", "bachelor programs", "bsc maths", "bsc physics", "bsc chemistry", "bsc cs", "bsc statistics"],
    "block":[
    "Main block", "VB block", "Rk block", "Polytechnic Block", "Pharmacy block", "Degree block", "Giet 2nd campus"],
    "boarding_points":[
    "boarding point", "boarding points", "bus stop", "pickup point", "pickup locations", "transport", "bus",
    "rajahmundry", "rajanagaram", "peddapuram", "surampalem", "kakinada", "pitapuram", "anaparthi", "dwarapudi",
    "kovvuru", "madiki", "dowleswaram", "kadiyam", "vemagiri", "bommuru", "kadiyapulanka", "ravulapalem", "edidha",
    "mandapeta", "kesavaram", "transport department"],
    "course fee":[
    "course fee", "course fees", "fees", "fee", "tuition", "tuition fee", "tuition fees", "cost", "cost of course",
    "branch fee", "stream fee", "btech fee", "mtech fee", "mba fee", "mca fee", "per year", "annual fee", "pay", "charges",

    # Branch-specific keywords
    "cse fee", "ece fee", "eee fee", "civil fee", "mech fee", "it fee", "mining fee", "automobile fee", "mba fee",
    "mca fee", "m.tech fee", "software engineering fee", "vlsi fee", "embedded fee", "aiml fee", "ai ml fee",
    "data science fee"],
    "Cutoff":[
    "ap eapcet", "ap eamcet", "cutoff", "cut off", "closing rank", "closing ranks", "rank", "ranks", "last rank",
    "2023", "2024", "engineering cutoff", "admission rank", "giet cutoff", "giet college rank", "counseling rank",

    # Branches
    "mechanical engineering", "civil engineering", "agricultural engineering", "electrical and electronics engineering",
    "computer science and engineering", "electronics and communication engineering", "information technology",
    "artificial intelligence and machine learning", "data science", "pharmacy", "school of pharmacy",

    # Colleges/Institutions
    "giet", "giet college", "giet rajahmundry", "giet engineering college", "giet school of pharmacy",
    "global institute of engineering and technology", "gandhi institute for education and technology",
    "gandhi institute of excellent technocrats", "moinabad", "bhubaneswar",

    # Exams
    "ap eapcet", "ap eamcet", "jee main", "ojee", "counseling"],
    "hospital":[
    "hospital", "clinic", "medical", "medunit", "emergency", "emergency treatment", "treatment", "healthcare",
    "doctor", "doctors", "nurse", "nurses", "first aid", "medicine", "medicines", "health", "injury", "injuries",
    "sick", "ill", "illness", "pharmacy", "available medicines", "medical help"],
    "juice_shop ":[
    "juice", "juice shop", "juices", "fruit juice", "fresh juice", "refreshments", "drinks", "beverages",
    "smoothie", "cool drinks", "milkshake", "lassi", "ice cream", "ice creams", "cold items", "shakes",

    # Specific juice names
    "mango", "pineapple", "badham", "dry fruits", "grapes", "musk melon", "apple", "banana", "blueberry",
    "strawberry"],
    "zerox": [
    "xerox", "zerox", "photocopy", "copy shop", "copying", "xerox center", "print", "printing", "scanner",
    "scanning", "document copy", "records", "file copy", "stationery", "books", "pens", "notebooks", "supplies",
    "sanitary items", "sanitary", "xerox machine", "xerox shop", "xerox facility", "record copy"],
    "distance":[
    "distance", "how far", "how many meters", "meters", "metres", "from main campus", "campus distance",
    "location distance", "walk", "walking distance", "near", "nearby", "far", "location", "how far is",

    # Specific places/buildings
    "rk block", "polytechnic block", "pharmacy block", "giet2", "giet 2nd campus", "degree block",
    "xerox shop", "food court", "juice shop", "yumpies", "girls hostel", "boys hostel", "mess", "central food court"]


}



class ChatService:
    """Service class for handling chat operations"""

    @staticmethod
    def translate_text(text, source_lang, target_lang):
        """Translate text between languages"""
        try:
            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        except Exception as e:
            print(f"Translation Error: {e}")
            return text

    @staticmethod
    def calculate_relevance_score(query_lower, topic_keywords):
        """Calculate relevance score for topic matching"""
        score = 0
        words = query_lower.split()
        for keyword in topic_keywords:
            if keyword in query_lower:
                score += 2 if keyword in words else 1
        return score

    @staticmethod
    def find_best_topic(query):
        """Find the most relevant topic based on query"""
        query_lower = query.lower()

        topic_scores = {
            topic: ChatService.calculate_relevance_score(query_lower, keywords)
            for topic, keywords in TOPIC_KEYWORDS.items()
            if ChatService.calculate_relevance_score(query_lower, keywords) > 0
        }

        if not topic_scores:
            return None

        best_topic = max(topic_scores, key=topic_scores.get)

        # Avoid generic "about" if other specific topics match
        if best_topic == "about" and len(topic_scores) > 1:
            topic_scores.pop("about")
            best_topic = max(topic_scores, key=topic_scores.get)

        return best_topic

    @staticmethod
    def get_ai_response(query):
        """Get response from Gemini AI"""
        try:
            prompt = f"""
            You are a helpful college enquiry assistant for Godavari Institute of Engineering and Technology (GIET).
            User Question: {query}
            Provide a helpful, concise, and factual response.
            """
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            return "I'm sorry, I couldn't process that right now."

    @staticmethod
    def generate_audio(text, lang_code):
        """Generate audio file from text"""
        try:
            tts = gTTS(text=text, lang=lang_code)
            filename = f"voice_{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            tts.save(filepath)
            return f"/static/{filename}"
        except Exception as e:
            print(f"TTS error: {e}")
            return None


# Routes
@app.route('/')
def index():
    """Home page route"""
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for processing user messages"""
    data = request.get_json()
    user_text = data.get('text', '')
    lang_code = data.get('lang', 'en')

    print(f"[User Input] [{lang_code}]: {user_text}")

    # Translate user input to English
    translated_query = ChatService.translate_text(user_text, lang_code, 'en')

    # Find best matching topic
    best_topic = ChatService.find_best_topic(translated_query)

    # Get response
    if best_topic and best_topic in COLLEGE_DATA:
        response_en = COLLEGE_DATA[best_topic]
    else:
        response_en = ChatService.get_ai_response(translated_query)

    # Translate response back to user's language
    translated_response = ChatService.translate_text(response_en, 'en', lang_code)

    # Generate audio
    audio_url = ChatService.generate_audio(translated_response, lang_code)

    return jsonify({
        'response': translated_response,
        'audio_url': audio_url
    })


def open_browser():
    """Open browser automatically"""
    webbrowser.open(f"http://{Config.HOST}:{Config.PORT}")


def setup_directories():
    """Create necessary directories"""
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


if __name__ == "__main__":
    setup_directories()

    # Open browser after a delay
    threading.Timer(1.0, open_browser).start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)