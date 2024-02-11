import streamlit as st
import openai
from streamlit_player import st_player
st.set_page_config(
    page_title="AI driven personlized diet and exercise model",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# Sidebar for OpenAI API Key Input
st.sidebar.title('Insert OpenAI API Key')
# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("https://c4.wallpaperflare.com/wallpaper/835/56/964/fitness-desktop-nexus-wallpaper-preview.jpg");
    background-size: cover;
    filter: blur(2px);  /* Adjust the blur amount */
    z-index: 0;
}
.title-wrapper {
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 2;
}
.title {
    text-align: center;
    width: 100%;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# Title centered on the page
st.markdown('<div class="title-wrapper"><h1 class="title">Personalized Diet and Fitness</h1></div>', unsafe_allow_html=True)
st.markdown(background_image, unsafe_allow_html=True)

user_openai_key = st.sidebar.text_input('Enter OpenAI API Key (Please):')

# Use the user-provided key if available, otherwise use the secret key
openai_api_key = user_openai_key if user_openai_key else st.secrets["OPENAI_API_KEY"]

# Set the OpenAI API key
openai.api_key = openai_api_key

# Function to calculate TDEE
def calculate_tdee(height, weight, activity_level, goal, age, units):
    # Convert height and weight to centimeters and kilograms
    if units == 'inches/lbs':
        height_cm = height * 2.54
        weight_kg = weight * 0.453592
    else:  # Assuming the other option is 'cm/kg'
        height_cm = height
        weight_kg = weight

    # Calculate BMR using Mifflin-St Jeor Equation
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5

    # Multiply by activity factor
    tdee = bmr * activity_level

    return tdee


# Introduction
st.write("""
Welcome to AI-based Personalized Diet and Fitness system, your personal guide to achieving the body of your dreams!
""")

# User Input for Workout Goals
goal = st.selectbox('Choose Your Fitness Goal', ['Weight Loss', 'Muscle Gain', 'Maintenance'])

# User Input for Dietary Preferences
diet = st.multiselect('Select Dietary Preferences (Optional)', ['Vegan', 'Keto', 'Low-Carb', 'High-Carb', 'Carb-Cycling', 'Gluten-Free'])

# Items in Fridge (for personalized diet recommendations)
fridge_items = st.text_area('Items in Your Fridge (Optional, leave empty if you only want a workout regimen)', value='', placeholder='E.g., eggs, chicken, broccoli, almonds...')

# Preferred Training Styles
training_styles = st.multiselect('Select Your Preferred Training Style - You can mix and match up to 3 trainers thanks to AI (Optional)', [
    'Arnold Schwarzenegger – Volume Training and Classic Physique',
    'Mike Mentzer – High-Intensity Training (HIT)',
    'Jay Cutler – Balanced Approach with Emphasis on Symmetry',
    'Dorian Yates – HIT with Blood and Guts Training',
    'Frank Zane – Focus on Proportion and Aesthetics',
    'Ronnie Coleman – High Volume and Heavy Lifting',
    'Lee Haney – Stimulate, Don\'t Annihilate; Emphasis on Recovery',
    'Calisthenics – Bodyweight Training for Strength and Flexibility',
    'Rich Gaspari – Pre-Exhaustion Training with Intensity',
    'Lou Ferrigno – Power Bodybuilding with Heavy Weights',
    'Sergio Oliva – Classic Mass Building with Frequent Training',
    'Larry Scott – Focus on Arms and Shoulders',
    'Tom Platz – High Volume Leg Specialization',
    'Flex Wheeler – Quality over Quantity; Focus on Form',
    'Phil Heath – Scientific Approach with Attention to Detail',
    'Chris Bumstead – Classic Physique with Modern Training',
    'Kai Greene – Mind-Muscle Connection and Artistic Expression',
    'CrossFit – Functional Fitness with Varied High-Intensity Workouts',
    'Powerlifting – Focus on Strength and Power',
    'Yoga – Focus on Flexibility and Mindfulness',
    'Pilates – Focus on Core Strength and Posture',
    'HIIT – High-Intensity Interval Training',
    'Fasted Cardio – Cardio on an Empty Stomach',
    'Kickboxing – Martial Arts and Cardio',
    'Boxing – Martial Arts and Cardio',
    'Muay Thai – Martial Arts and Cardio',
    'Karate – Martial Arts',
    'Taekwondo – Martial Arts',
    'Zumba – Dance Fitness',
], max_selections=3)

# Height and Weight Inputs
units = st.selectbox('Choose Your Units', ['inches/lbs', 'cm/kg'])

if units == 'inches/lbs':
    height_description = 'Enter Your Height (e.g., 68 inches)'
    weight_description = 'Enter Your Weight (e.g., 160 lbs)'
else:  # Assuming the other option is 'cm/kg'
    height_description = 'Enter Your Height (e.g., 172 cm)'
    weight_description = 'Enter Your Weight (e.g., 73 kg)'

height = st.number_input(height_description, min_value=0, max_value=300, step=1)
weight = st.number_input(weight_description, min_value=0, max_value=500, step=1)
age = st.number_input('Enter Your Age', min_value=0, max_value=120, step=1)

activity_levels = {
    "Sedentary (little to no exercise)": 1.2,
    "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
    "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
    "Very active (hard exercise/sports 6-7 days a week)": 1.725,
    "Super active (very hard exercise/sports & physical job or training twice a day)": 1.9
}
activity_level = st.selectbox('Choose Your Activity Level', list(activity_levels.keys()))
activity_factor = activity_levels[activity_level]

def generate_plan(goal, diet, fridge_items, training_styles, tdee, age):
    messages = [
        {
            "role": "system",
            "content": f"You are an extremely detailed AI, knowledgeable in bodybuilding, fitness, and dietetics, and an expert! You only respond ethically."
        },
        {
            "role": "user",
            "content": f"My dietary preferences are {diet}. Create the perfect curated plan from {training_styles}. If there is anything in my fridge {fridge_items}, please include a meal plan, if not, don't mention the fridge being empty. My TDEE is {tdee} and I am {age} years old. My fitness goal is {goal}. Please give me accurate responses based on my information. If I withheld dietary preference or training style, IGNORE IT and carry on with a generic response. Do not give me any extra info, just respond as the trainers or mix of trainers and give the workout plan based on daily basis and the philosophy along with some things to research if need be and quotes from the trainers if there are any. Be extremely detailed and straight to the point, give the diet and excercise plans on day to day basis."
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )

    return response['choices'][0]['message']['content']
# Define a mapping of exercises to video links (example data)

if st.button('Generate Plan'):
    if not height or not weight or not age or not activity_level:
        st.error('Please fill in all required fields before generating the plan.')
    else:
        with st.spinner('Generating...'):
            tdee = calculate_tdee(height, weight, activity_levels[activity_level], goal, age, units)
            if tdee:
                plan = generate_plan(goal, diet, fridge_items, training_styles, tdee, age)
                if plan:
                    # Container for displaying the plan output
                    with st.container():
                        st.markdown(plan)
                        # Download Button
                        download_plan = st.download_button(
                            label="Download Plan",
                            data=plan,
                            file_name="Personalized_Plan.txt",
                            mime="text/plain"
                        )
                        if download_plan:
                            st.success("Plan downloaded successfully!")
                        # Display exercise videos
                        st_player("https://www.youtube.com/watch?v=eiMOxvZKyvM")
                        st_player("https://www.youtube.com/watch?v=YaXPRqUwItQ")
                        st_player("https://www.youtube.com/watch?v=0Av02v-gMw8")
                        st_player("https://www.youtube.com/watch?v=OzrQdH4VEIs")
                        st_player("https://www.youtube.com/watch?v=q7rCeOa_m58")
                        st_player("https://www.youtube.com/watch?v=1tHZ-hUH2P8")
                        st_player("https://www.youtube.com/watch?v=5kstCo2lZW0")
                        st_player("https://www.youtube.com/watch?v=8PwoytUU06g")
                        
                else:
                    st.error('An error occurred while generating your plan. Please try again later.')
            else:
                st.error('An error occurred while calculating your plan. Please make sure all inputs are correct.')
