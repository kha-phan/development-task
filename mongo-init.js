// Create admin user
db.createUser({
  user: "adminUser",
  pwd: "adminPassword",
  roles: [
    { role: "readWrite", db: "admin" },
    { role: "dbAdmin", db: "admin" },
    { role: "userAdmin", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
});

// Switch to admin database
db = db.getSiblingDB('admin');

// Create travel_recommendations database
db.createCollection('travel_recommendations');

// Switch to travel_recommendations database
db = db.getSiblingDB('travel_recommendations');

// Create tasks collection
db.createCollection('tasks');

// Create a new user and grant full permissions on the travel_recommendations database
db.createUser({
  user: "devUser",
  pwd: "devPassword",
  roles: [{ role: "readWrite", db: "travel_recommendations" }]
});
