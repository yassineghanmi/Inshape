from django.shortcuts import render, redirect
from .forms import RoutineForm  # Updated import for the new RoutineForm
from .models import Routine  # Import your Routine model
import google.generativeai as genai

# Configure your AI model
genai.configure(api_key="AIzaSyDd9RRJuKh0b4RDo45KMV3mPuqkVf8upe0")  # Replace with your actual API key
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}
model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

def workout_view(request):
    if request.method == 'POST':
        # Collect input data from the form
        goal = request.POST.get('goal')
        experience_level = request.POST.get('experience_level')
        duration = request.POST.get('duration')
        workout_type = request.POST.get('workout_type')
        target_muscle_groups = request.POST.get('target_muscle_groups').split(",")  # Assuming comma-separated input
        equipment_needed = request.POST.get('equipment_needed').split(",")  # Assuming comma-separated input
        sessions_per_week = request.POST.get('sessions_per_week')

        # Prepare the workout data dictionary
        workout_data = {
            "goal": goal,
            "experience_level": experience_level,
            "duration": duration,
            "workout_type": workout_type,
            "target_muscle_groups": target_muscle_groups,
            "equipment_needed": equipment_needed,
            "sessions_per_week": sessions_per_week
        }

        # Format the prompt for the AI
        prompt = f"Recommend me a workout routine using this data: {workout_data}"

        # Start a chat session and send the prompt to the AI
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)

        # Get the AI's response
        generated_routine = response.text  # The generated routine details
        
        # Redirect to the preview page with the generated routine
        return render(request, 'routine_planner/workout_result.html', {
            'generated_routine': generated_routine
        })

    return render(request, 'routine_planner/workout_form.html')


def save_routine(request):
    if request.method == 'POST':
        # Collect routine name and created_by from user input
        routine_name = request.POST.get('routine_name')
        created_by = request.POST.get('created_by')
        details = request.POST.get('generated_routine')  # The AI-generated routine

        # Save the generated routine to the database
        routine = Routine(
            name=routine_name,
            created_by=created_by,
            details=details
        )
        routine.save()

        return redirect('success_url')  # Replace with your success URL or template

    return redirect('workout_form')  # Or wherever you want to redirect if the method is not POST
def success_view(request):
    routines = Routine.objects.all()  # Retrieve all routines from the database
    return render(request, 'routine_planner/success.html', {'routines': routines})