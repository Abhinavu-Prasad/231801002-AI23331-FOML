import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean

# Skill categories for Conexxaa
categories = [
    "Technical Proficiency", "Project Management", "Data Analysis", 
    "Communication & Collaboration", "Problem-Solving", "Leadership & Initiative", 
    "Adaptability & Flexibility", "Client Relationship Management", 
    "Research & Development", "Industry-Specific Knowledge"
]

# Default company profiles with roles and their corresponding skill requirements
companies = {
    "Tata Consultancy Services (TCS)": {
        "Software Engineer": [10, 6, 7, 7, 9, 5, 8, 6, 6, 7],
        "IT Analyst": [9, 7, 8, 9, 8, 7, 7, 8, 5, 8]
    },
    "Infosys": {
        "Software Developer": [10, 6, 7, 8, 9, 6, 8, 7, 7, 7],
        "Systems Engineer": [9, 7, 6, 8, 8, 6, 7, 7, 6, 7]
    },
    "Wipro": {
        "Software Engineer": [10, 5, 7, 7, 9, 6, 8, 6, 5, 7],
        "Data Scientist": [10, 6, 10, 8, 9, 7, 7, 6, 8, 7]
    },
    "Accenture": {
        "Technology Consultant": [8, 7, 6, 9, 8, 7, 8, 9, 7, 8],
        "Software Engineer": [10, 6, 7, 7, 9, 6, 8, 6, 5, 7]
    },
    "Zoho": {
        "Software Developer": [10, 6, 7, 7, 9, 6, 8, 6, 6, 7],
        "Product Engineer": [10, 6, 7, 8, 9, 7, 8, 6, 8, 7]
    }
}

# Minimum skill requirement thresholds for eligibility
skill_thresholds = {
    "Technical Proficiency": 7,
    "Project Management": 5,
    "Data Analysis": 6,
    "Communication & Collaboration": 6,
    "Problem-Solving": 7,
    "Leadership & Initiative": 5,
    "Adaptability & Flexibility": 6,
    "Client Relationship Management": 6,
    "Research & Development": 5,
    "Industry-Specific Knowledge": 5
}

# Function to calculate the rank based on similarity of skills using Euclidean distance
def match_companies(student_skills, selected_companies):
    rankings = []
    ineligible_feedback = []
    
    for company, roles in companies.items():
        if company not in selected_companies:
            continue  # Skip companies that are not in the selected list
            
        for role, requirements in roles.items():
            # Check if student meets the minimum skill thresholds for the role
            below_threshold = [
                categories[i] for i in range(len(student_skills)) 
                if student_skills[i] < skill_thresholds[categories[i]]
            ]
            
            if below_threshold:
                # Suggest the most closely related skills that need improvement (top 2)
                closest_skills = get_top_closest_skills(student_skills, below_threshold)
                ineligible_feedback.append((company, role, closest_skills))
                continue  # Skip this company/role if the student doesn't meet the eligibility
            
            # Calculate Euclidean distance if eligible
            distance = np.linalg.norm(np.array(student_skills) - np.array(requirements))
            rankings.append((company, role, distance))
    
    # Sort by Euclidean distance (lower is better)
    rankings.sort(key=lambda x: x[2])
    
    return rankings, ineligible_feedback

# Function to find the top 2 closest skills to the threshold
def get_top_closest_skills(student_skills, below_threshold):
    skill_gaps = {}
    
    for skill in below_threshold:
        skill_index = categories.index(skill)
        gap = skill_thresholds[skill] - student_skills[skill_index]
        skill_gaps[skill] = gap
    
    # Sort by gap and return the top 2 closest skills
    sorted_skills = sorted(skill_gaps.items(), key=lambda x: x[1])[:2]
    return [skill for skill, _ in sorted_skills]

# Input: Student's skill profile
student_skills = [int(input(f"Enter your skill level for {category} : ")) for category in categories]

# Specify which companies to focus on (TCS and Infosys)
selected_companies = ["Tata Consultancy Services (TCS)", "Infosys"]

# Get matching companies and roles
rankings, ineligible_feedback = match_companies(student_skills, selected_companies)

# Display rankings and ineligible feedback for the selected companies
if rankings:
    print("\nEligible Matches:")
    for i, (company, role, distance) in enumerate(rankings[:3], 1):  # Display only top 3 matches
        print(f"Rank {i}: {company} - {role}")
else:
    print("No eligible matches found based on your skills.")

# Provide detailed feedback only on the non-eligible roles for the selected companies
print("\nEligibility Feedback for Non-Eligible Companies and Roles:")
for company, roles in companies.items():
    if company not in selected_companies:
        continue  # Skip companies that are not in the selected list
        
    for role, requirements in roles.items():
        # Check eligibility
        below_threshold = [
            categories[i] for i in range(len(student_skills)) 
            if student_skills[i] < skill_thresholds[categories[i]]
        ]
        
        if below_threshold:
            # Suggest top 2 closest skills to improve
            closest_skills = get_top_closest_skills(student_skills, below_threshold)
            print(f"{company} - {role}: Suggest improving: {', '.join(closest_skills)}")

# Plotting the skills comparison for top ranked company and role
if rankings:
    top_match = rankings[0]
    top_company = top_match[0]
    top_role = top_match[1]
    top_requirements = companies[top_company][top_role]

    # Plotting the skills comparison
    x = range(len(categories))

    plt.figure(figsize=(12, 6))

    # Plot the student's skills
    plt.plot(x, student_skills, marker='o', label='Student', color='blue')

    # Plot the top company's skill requirements for the matched role
    plt.plot(x, top_requirements, marker='o', label=f'{top_company} - {top_role}', color='orange')

    # Adding titles and labels
    plt.title(f'Skill Profile Comparison: Student vs. {top_company} - {top_role}')
    plt.xlabel('Skill Categories')
    plt.ylabel('Skill Ratings')
    plt.xticks(x, categories, rotation=45, ha='right')
    plt.ylim(0, 10)
    plt.axhline(y=0, color='k', linestyle='--', lw=1)
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
else:
    print("No eligible matches.")
