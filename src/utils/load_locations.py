from langchain_core.documents import Document
from uuid import uuid4

locations = [
    ("Statue of Liberty", "An iconic outdoor monument in New York Harbor offering city views from the crown.", "outdoor", "New York"),
    ("Smithsonian National Air and Space Museum", "A museum in Washington, D.C. with exhibits on aviation and space exploration.", "indoor", "Washington, D.C."),
    ("Yosemite National Park", "A stunning outdoor park in California featuring waterfalls, cliffs, and giant sequoias.", "outdoor", "California"),
    ("Metropolitan Museum of Art", "A vast indoor museum in New York City housing art from around the world.", "indoor", "New York"),
    ("Golden Gate Park", "A large outdoor park in San Francisco with gardens, trails, and cultural attractions.", "outdoor", "San Francisco"),
    ("Shedd Aquarium", "An indoor aquarium in Chicago featuring marine life from around the globe.", "indoor", "Chicago"),
    ("Grand Teton National Park", "An outdoor park in Wyoming known for its dramatic mountain range and wildlife.", "outdoor", "Wyoming"),
    ("Museum of Modern Art (MoMA)", "A major indoor art museum in New York City focused on modern works.", "indoor", "New York"),
    ("Zion National Park", "A Utah outdoor park with red cliffs, canyons, and scenic hikes.", "outdoor", "Utah"),
    ("Georgia Aquarium", "An indoor attraction in Atlanta with large exhibits of ocean life.", "indoor", "Atlanta"),
    ("Bryce Canyon National Park", "An outdoor park in Utah known for its unique rock formations called hoodoos.", "outdoor", "Utah"),
    ("Art Institute of Chicago", "An indoor art museum with an extensive collection of paintings and sculptures.", "indoor", "Chicago"),
    ("Rocky Mountain National Park", "An outdoor destination in Colorado with alpine lakes and wildlife.", "outdoor", "Colorado"),
    ("Getty Center", "An indoor/outdoor art campus in Los Angeles offering art and architecture.", "indoor", "Los Angeles"),
    ("Glacier National Park", "A Montana outdoor park with rugged terrain and scenic vistas.", "outdoor", "Montana"),
    ("American Museum of Natural History", "A New York indoor museum with fossils, dioramas, and a planetarium.", "indoor", "New York"),
    ("Acadia National Park", "An outdoor Maine park offering coastline views and forested hiking trails.", "outdoor", "Maine"),
    ("National Gallery of Art", "An indoor museum in Washington, D.C. with European and American masterpieces.", "indoor", "Washington, D.C."),
    ("Death Valley National Park", "An outdoor park in California known for its extreme heat and desert beauty.", "outdoor", "California"),
    ("Liberty Science Center", "An indoor science museum in New Jersey with hands-on exhibits.", "indoor", "New Jersey"),
    ("Mount Rainier National Park", "An outdoor park in Washington with forests, waterfalls, and glaciers.", "outdoor", "Washington"),
    ("Exploratorium", "An indoor interactive science museum in San Francisco.", "indoor", "San Francisco"),
    ("Great Smoky Mountains National Park", "An outdoor park on the border of North Carolina and Tennessee with misty mountains.", "outdoor", "Tennessee"),
    ("California Science Center", "An indoor museum in Los Angeles with a space shuttle and science exhibits.", "indoor", "Los Angeles"),
    ("White Sands National Park", "An outdoor park in New Mexico featuring vast dunes of gypsum sand.", "outdoor", "New Mexico"),
    ("The Broad", "An indoor contemporary art museum in Los Angeles.", "indoor", "Los Angeles"),
    ("Everglades National Park", "A Florida outdoor park with wetlands, alligators, and airboat tours.", "outdoor", "Florida"),
    ("Seattle Aquarium", "An indoor aquarium with marine animals and ocean exhibits.", "indoor", "Seattle"),
    ("Arches National Park", "An outdoor park in Utah with natural sandstone arches.", "outdoor", "Utah"),
    ("Boston Museum of Science", "An indoor museum with science and technology exhibits.", "indoor", "Boston"),
    ("Joshua Tree National Park", "An outdoor California park with desert landscapes and unique trees.", "outdoor", "California"),
    ("Whitney Museum of American Art", "An indoor art museum in New York City focusing on American artists.", "indoor", "New York"),
    ("Crater Lake National Park", "An outdoor park in Oregon featuring a deep blue lake in a volcanic crater.", "outdoor", "Oregon"),
    ("Tech Interactive", "An indoor science and technology center in San Jose.", "indoor", "San Jose"),
    ("Badlands National Park", "An outdoor park in South Dakota with eroded rock formations and fossils.", "outdoor", "South Dakota"),
    ("Children’s Museum of Indianapolis", "The largest indoor children’s museum in the world.", "indoor", "Indianapolis"),
    ("Big Bend National Park", "An outdoor park in Texas with desert, mountains, and the Rio Grande.", "outdoor", "Texas"),
    ("Franklin Institute", "An indoor science museum in Philadelphia with interactive exhibits.", "indoor", "Philadelphia"),
    ("Sequoia National Park", "An outdoor California park home to giant sequoia trees.", "outdoor", "California"),
    ("Detroit Institute of Arts", "An indoor museum with collections from around the world.", "indoor", "Detroit"),
    ("Denali National Park", "An Alaskan outdoor park with North America's tallest peak.", "outdoor", "Alaska"),
    ("Perot Museum of Nature and Science", "An indoor science museum in Dallas.", "indoor", "Dallas"),
    ("Haleakalā National Park", "An outdoor park in Hawaii featuring a massive volcanic crater.", "outdoor", "Hawaii"),
    ("National WWII Museum", "An indoor museum in New Orleans focusing on World War II.", "indoor", "New Orleans"),
    ("Redwood National and State Parks", "An outdoor park with towering redwoods in California.", "outdoor", "California"),
    ("Museum of the American Revolution", "An indoor museum in Philadelphia.", "indoor", "Philadelphia"),
    ("Olympic National Park", "An outdoor park in Washington state with diverse ecosystems.", "outdoor", "Washington"),
    ("Houston Museum of Natural Science", "An indoor science museum in Houston.", "indoor", "Houston")
]

DOCUMENTS = [
    Document(
        page_content = description,
        metadata = {"name": name,
                    "description": description,
                    "category": category,
                    "city": city
                    }
    ) 
    for name, description, category, city in locations
]

UUIDS = [str(uuid4()) for _ in range(len(DOCUMENTS))]