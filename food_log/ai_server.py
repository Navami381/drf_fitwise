from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

# Step 1: Authenticate
client = genai.Client(api_key=api_key)


def get_diet_plan(response_data):

    monthly_total = response_data.get("monthly_total")
    monthly_meal_summary = response_data.get("monthly_meal_summary")

    meal_summary_text = ""

    for di in monthly_meal_summary:
        meal_summary_text += (
            f"- {di.get('meal_type')} : "
            f"{di.get('total')} calories\n"
        )

    print(meal_summary_text)

    # Step 2: Create the prompt
    prompt = f"""
    Act as an expert nutrition advisor specializing in
    balanced diets and healthy eating habits in Kerala, India.

    Here is my monthly meal summary:

    - Total Monthly Calorie Intake: {monthly_total}
    - Meal-Wise Calorie Breakdown:
    {meal_summary_text}

    Based on this data, generate a practical personalized
    diet plan with the following:

    1. Meal Analysis:
       Analyze the monthly calorie intake and meal-wise
       calorie distribution. Identify possible imbalances.

    2. Optimized Daily Diet Plan:
       Suggest a balanced daily meal plan including
       breakfast, lunch, dinner, and snacks.
       Include suitable food options commonly available
       in Kerala, such as rice, puttu, idli, dosa,
       vegetables, fruits, pulses, and eggs.

    3. Healthy Eating Recommendations:
       Suggest practical ways to improve meal balance,
       food variety, and portion control.

    4. Kerala-Specific Food Suggestions:
       Recommend affordable, locally available foods
       that can support balanced nutrition.

    5. Weekly Meal Suggestions:
       Provide a simple 7-day meal plan with varied
       and nutritious food choices.

    Important:
    - Do not assume that the user needs to lose weight.
    - Do not invent missing health or personal details.
    - Explain that calorie requirements depend on age,
      activity level, health status, and individual goals.
    - Provide general nutrition guidance, not medical advice.
    """

    # Step 3: Generate the AI diet plan
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    # Step 4: Return the generated diet plan
    return response.text