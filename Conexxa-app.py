import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

# Sample company dataset
company_data = {
    'Company': ['Acme Inc.', 'Globex Corporation', 'TechSavvy Solutions', 'DataDynamic', 'EnergySmart'],
    'Industry': ['Technology', 'Manufacturing', 'IT Services', 'Data Analytics', 'Energy'],
    'Skills Needed': [['Python', 'Data Analysis', 'Machine Learning'],
                     ['Project Management', 'CAD', 'Mechanical Engineering'],
                     ['Web Development', 'Cloud Computing', 'Cybersecurity'],
                     ['SQL', 'Statistics', 'Visualization'],
                     ['Renewable Energy', 'Electrical Engineering', 'Energy Efficiency']],
    'Openings': [5, 3, 8, 4, 2]
}

company_df = pd.DataFrame(company_data)

def get_user_profile():
    print("Welcome to Mentor Connect!")
    print("Please fill out your profile to get matched with companies.")

    name = input("What is your name? ")
    skills = input("What are your skills (comma-separated)? ").split(',')
    interests = input("What are your academic interests (comma-separated)? ").split(',')
    goals = input("What are your career goals? ")

    return {'Name': name, 'Skills': [skill.strip() for skill in skills],
            'Interests': [interest.strip() for interest in interests], 'Goals': goals}

def match_companies(user_profile):
    # Create a feature matrix from the company data
    X = []
    for skills in company_data['Skills Needed']:
        skill_vector = [int(skill in skills) for skill in user_profile['Skills']]
        X.append(skill_vector)
    X = pd.DataFrame(X)

    # Normalize the feature matrix
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the KNN model
    knn = NearestNeighbors(n_neighbors=3)
    knn.fit(X_scaled)

    # Find the closest companies to the user's profile
    user_skills = [int(skill in user_profile['Skills']) for skill in company_data['Skills Needed'][0]]
    user_skills_scaled = scaler.transform([user_skills])
    distances, indices = knn.kneighbors(user_skills_scaled)

    # Return the matched company names
    return [company_data['Company'][i] for i in indices[0]]

def main():
    user_profile = get_user_profile()
    print("\nYour profile:")
    for key, value in user_profile.items():
        print(f"{key}: {value}")

    matches = match_companies(user_profile)
    if matches:
        print("\nTop 3 matching companies:")
        for company in matches:
            print(f"- {company}")
    else:
        print("\nSorry, no companies currently match your profile. Please try again later.")

if __name__ == "__main__":
    main()
