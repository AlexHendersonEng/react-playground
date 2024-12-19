# Import packages/modules
from flask import request, jsonify
from config import app, db
from models import Contact

# Get (GET) contacts endpoint
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # Get all contacts
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts}), 200

# Create (POST) contacts endpoint
@app.route("/create_contact", methods=["POST"])
def create_contact():
    # Get data from request
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # Throw error if data not provided
    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email."}),
            400
        )

    # Create new contact
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "User created."}), 201

# Update (PUT) contact endpoint
@app.route("/update_contact/<int:user_id>", methods=["PUT"])
def update_contact(user_id):
    # Get contact
    contact = Contact.query.get(user_id)

    # Error handling
    if not contact:
        return jsonify({"message": "User not found."}), 404

    # Update data
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify({"message": "User data updated."}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # Get contact
    contact = Contact.query.get(user_id)

    # Error handling
    if not contact:
        return jsonify({"message": "User not found."}), 404

    # Delete user data
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "User deleted."}), 200

# Run Flask application
if __name__ == "__main__":
    # Create database
    with app.app_context():
        db.create_all()

    # Run application
    app.run(host='0.0.0.0', port=5000, debug=True)