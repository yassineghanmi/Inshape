from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RoutineForm  # Updated import for the new RoutineForm
from .models import Routine  # Import your Routine model
import google.generativeai as genai
import json  # Make sure to import the json module

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


def delete_routine(request, id):
    routine = get_object_or_404(Routine, id=id)
    routine.delete()
    return redirect('success_url')


class RoutineDetailView(View):
    def get(self, request, id):
        routine = get_object_or_404(Routine, id=id)

        # Deserialize the JSON string in routine.details
        routine.details = json.loads(routine.details)  # Ensure 'details' is a JSON string in the database

        return render(request, 'routine_planner/routine_detail.html', {'routine': routine})

from django.contrib.auth.decorators import login_required
@login_required(login_url='/accounts/login')
def workout_view(request):
    if request.method == 'POST':
        # Collect input data from the form
        goal = request.POST.get('goal')
        experience_level = request.POST.get('experience_level')
        duration = request.POST.get('duration')
        workout_type = request.POST.get('workout_type')
        # Safely get the 'target_muscle_groups' and 'equipment_needed' values
        target_muscle_groups = request.POST.get('target_muscle_groups', '')  # Default to an empty string if not present
        equipment_needed = request.POST.get('equipment_needed', '')  # Default to an empty string if not present

        # Only split if the value is not empty
        target_muscle_groups = target_muscle_groups.split(",") if target_muscle_groups else []
        equipment_needed = equipment_needed.split(",") if equipment_needed else []
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
        prompt = (
            f"Create a workout routine based on this data {workout_data}, ensuring it follows this exact JSON structure. "
            "Do not alter any fields or structure; fill in the fields with specific details as applicable to the user’s input. "
            "Use the same field names, order, and structure as in the template provided below:\n"
            "{\n"
            "  \"routine\": {\n" \
            "    \"Monday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Tuesday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Wednesday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Thursday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Friday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Saturday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    },\n" \
            "    \"Sunday\": {\n" \
            "      \"name\": \"\",\n" \
            "      \"duration\": 0,\n" \
            "      \"exercises\": [\n" \
            "        {\n" \
            "          \"name\": \"\",\n" \
            "          \"sets\": 0,\n" \
            "          \"reps\": \"\",\n" \
            "          \"rest\": 0,\n" \
            "          \"equipment\": \"\"\n" \
            "        }\n" \
            "      ],\n" \
            "      \"cardio\": {\n" \
            "        \"type\": \"\",\n" \
            "        \"duration\": 0,\n" \
            "        \"intensity\": \"\"\n" \
            "      }\n" \
            "    }\n" \
            "  },\n" \
            "  \"notes\": \"\"\n" \
            "}"
        )

        # Start a chat session and send the prompt to the AI
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)

        # Get the AI's response
        generated_routine = response.text  # The generated routine details
        generated_routinejson = json.loads(generated_routine)
        # Redirect to the preview page with the generated routine
        return render(request, 'routine_planner/workout_result.html', {
            'generated_routine': generated_routine,
            "json_routine": generated_routinejson,
        })

    return render(request, 'routine_planner/workout_form.html')


def save_routine(request):
    if request.method == 'POST':
        routine_name = request.POST.get('routine_name')
        created_by = request.user
        details = request.POST.get('generated_routine')

        if not details:
            print("Details are empty!")

        # Debugging: Print out the values
        print(f"Routine Name: {routine_name}, Created By: {created_by}, Details: {details}")

        # Deserialize the details from JSON string to dict
        details_dict = json.loads(details)

        routine = Routine(
            name=routine_name,
            created_by=created_by,
            details=json.dumps(details_dict)  # Save as JSON string in the database
        )
        routine.save()

        return redirect('success_url')

    return redirect('workout_form')


def success_view(request):
    if request.user.is_authenticated:
        # If the user is logged in, filter routines by the logged-in user
        routines = Routine.objects.filter(created_by=request.user)
    else:
        # If the user is not logged in, get all routines
        routines = Routine.objects.all()

    # Parse the details for each routine
    for routine in routines:
        try:
            routine.details = json.loads(routine.details)  # Convert JSON string to dict
        except json.JSONDecodeError:
            routine.details = {}  # If parsing fails, set to empty dict or handle accordingly

    return render(request, 'routine_planner/success.html', {'routines': routines})

def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            return redirect('routine_detail', id=routine.id)  # Use 'id' here
    else:
        form = RoutineForm(instance=routine)

    return render(request, 'routine_planner/edit_routine.html', {'form': form, 'routine': routine})
