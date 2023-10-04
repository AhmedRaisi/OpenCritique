# Mock database
# Mock database
movies_initial = [
    "The Shawshank Redemption", "The Godfather", "Pulp Fiction", "The Dark Knight", "Inception",
    "Fight Club", "Forrest Gump", "The Matrix", "The Empire Strikes Back", "The Social Network",
    "Interstellar", "Coco", "The Grand Budapest Hotel", "Mad Max: Fury Road", "Moonlight",
    "Parasite", "The Revenant", "Whiplash", "The Big Short", "Django Unchained"
]

movie_filters = {
    "set_1": ["La La Land", "Toy Story", "Up", "Jurassic Park", "Avatar",
              "The Lord of the Rings: The Fellowship of the Ring", "A Beautiful Mind", "Gladiator", "Slumdog Millionaire", "Eternal Sunshine of the Spotless Mind",
              "Schindler's List", "Ratatouille", "WALL-E", "Inside Out", "Get Out",
              "Lady Bird", "Once Upon a Time in Hollywood", "The Irishman", "Birdman", "Blade Runner 2049"],
    
    "set_2": ["Casablanca", "Psycho", "Gone with the Wind", "Sunset Boulevard", "Citizen Kane",
              "Chinatown", "Vertigo", "The Silence of the Lambs", "Some Like It Hot", "Goodfellas",
              "Rosemary's Baby", "Taxi Driver", "M", "2001: A Space Odyssey", "12 Angry Men",
              "Seven Samurai", "The Bridge on the River Kwai", "Apocalypse Now", "Metropolis", "A Clockwork Orange"]
}

critics_db = {
    "Roger Ebert": ["La La Land", "Up", "Schindler's List", "Goodfellas", "The Shawshank Redemption", "Pulp Fiction", "The Dark Knight", "Fight Club", "Casablanca", "Vertigo"],
    "A.O. Scott": ["The Godfather", "The Matrix", "Mad Max: Fury Road", "The Social Network", "Eternal Sunshine of the Spotless Mind", "Ratatouille", "Psycho", "Some Like It Hot", "The Silence of the Lambs", "Chinatown"]
}

# The rest of the program remains unchanged.


# Helper function to choose movies
def choose_movies(movie_list):
    for idx, movie in enumerate(movie_list, 1):
        print(f"{idx}. {movie}")
    
    choices = []
    while len(choices) < 5:
        try:
            choice = int(input("Choose a movie by number: "))
            if 1 <= choice <= 20 and movie_list[choice-1] not in choices:
                choices.append(movie_list[choice-1])
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Enter a valid number.")
    return choices

# Start
print("Choose 5 movies from the following list:")
first_choices = choose_movies(movies_initial)

print("\nBased on your choices, choose 5 more movies from the following list:")
second_choices = choose_movies(movie_filters["set_1"] if sum(map(first_choices.count, movie_filters["set_1"])) > 2 else movie_filters["set_2"])

# Find the critic
matched_critic = None
for critic, movies in critics_db.items():
    if sum(map(second_choices.count, movies)) >= 3:
        matched_critic = critic
        break

if matched_critic:
    print(f"\nBased on your choices, we recommend {matched_critic}!")
    print(f"{matched_critic} recommends: {', '.join(critics_db[matched_critic])}")
else:
    print("\nSorry, we couldn't find a matching critic based on your choices.")
