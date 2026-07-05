# Project Architecture & Design Log
This file acts as the single source of truth for all major structural, database, and architectural decisions made during the development of this application.

### Core Purpose:
 We just need to be able to scan a bill and add the items to inventory. We should be able to create the shopping list from the inventory. Multiple people should be able to collaborate as a household and make the list

### Advanced feature breakdown
1. Scan bill and add to inventory.
2. Recite dish made and number of people which would remove items. Can also remove based on spoiled / thrown items manually.
3. Create shopping list collaborative. 
4. Shopping list can autopopulate based on items at min threshold levels.
5. App can send warnings about perishables.

### Learning / Basic breakdown for v1 launch
1. Basic add/ remove / update inventory manually.
2. Basic make shopping list collaboratively.

### Chat suggested flow:
1. Phase 1: Make a household model, inventory model, shopping list model. Implement the API.
2. Phase 2: Bill Scanner + Scale Up
3. Phase 3: Auto-populate shopping list
4. Phase 4: Auto-remove item from inventory based on recipe made
5. Phase 5: Collaborative syncing of inventory, shopping list

### My suggested workflow:

## Tech Stack

Backend: Django 5.2 + Django REST Framework
Purpose is to get comfortable with django so using it.
Database: SQLite v1 → PostgreSQL v2+
SQLite is good for MVP with less users, will pivot to PostgreSQL in phase 2.
Frontend: React + TypeScript
Good opportunity to practice design skills and review react concepts.
Auth: Django session-based (can swap to JWT tokens later)


#### Phase 1 (Weeks 1-2)

1. Django project setup with SQLite
   - Create Django project and apps (households, inventory, users)
   - Configure DRF, settings.py, requirements.txt

2. Data models & migrations
   - Define models: Household, HouseholdMember, Catalog, Inventory, ShoppingCart
   - Create migrations with constraints (uniqueness, foreign keys)
   - Test: verify constraints enforce correctly

3. Auth middleware & decorators
   - Session-based auth middleware (extract user from request)
   - Permission decorators: @is_household_member, @is_owner
   - Test: verify 401/403 responses work

4. API endpoints (in dependency order)
   - Households: POST, PATCH, DELETE
   - Members: POST, GET /me, PATCH, DELETE
   - Catalog: POST, GET list, GET one, PATCH, DELETE
   - Inventory: POST, GET list, GET one, PATCH, DELETE
   - Cart: POST, GET list, GET one, PATCH, DELETE (and DELETE all)

5. API testing (manual + unit tests)
   - Test each endpoint with valid/invalid inputs
   - Test auth checks (member vs owner)
   - Test uniqueness constraints (409 conflict)

6. React frontend (basic, feature-complete)
   - Login screen
   - Household switcher (GET /members/me)
   - Inventory CRUD screen
   - Cart CRUD screen
   - Multi-user test (two browsers, same household)

---

## Data Model

User Table (django native):
- UUID
- Name

Households Table:
- UUID
- HouseName
- created_at
- updated_at

HouseholdMember Table:
- User ID
- Household ID
- role - either owner, or member
- created_at
- updated_at

** Uniqueness constraint on <UserID, HouseholdID>

Catalog:
- Item name - string
- UUID - unique id for the item
- Type - constrained string [Frozen, Dairy, Pulses, ..]
- created at - date
- updated at - date
- HouseholdID - foreign key

Inventory:
- item_id (foreign key)
- household_id (foreign key)
- purchased on - date
- expiry date - date
- qty - decimal
- unit - options = ["Kg", "L", "ml", pieces]

Constraint: Uniqueness constraint of item_id, household_id, purchased_on, expiry_date.
And, qty > 0 constraint.

Shopping Cart Table:
- Household_id (foreign key)
- item_id (foreign key)
- qty_needed
- unit
- is_bought (bool)

Constraint: Uniqueness constraint of <item_id, household_id>

## API v1

By default in all API calls, the user should be authenticated.

### Status codes

- 400: validation error
- 401: unauthenticated access
- 403: forbidden (user does not have authorization)
- 404: not found
- 409: Record already exists
- 201: Created
- 
#### Endpoints to edit the Household Table

1. POST /households 
Create a new household, allowed for any authenticated user of app. adds the owner in the members table.

2. PATCH /households/{household-id}
Update name of the household , allowed for owner of household.
3. DELETE /households/{household-id}
Delete household , allowed for owner of household.

Future rules:
1. Max of 5 households per person

#### Endpoints to edit the Household Member Table

1. POST /households/{household-id}/members
Create a new household member entry. Can be done by owner of household for another user. User-id to add will be in body of request.
Does a check of the authenticated user identity performing the call.
2. GET /members/me
Get the user's associated households - all name details. Can be done by any authenticated user.
3. PATCH /households/{household-id}/members/{user-id}
Update the role of the member in the specific household. Can be done by the owner of household.
4. DELETE /households/{household-id}/members/{user-id}
Delete the household membership of the user. Verify if the user-id is member. Can be done by owner of the household. Owner
cannot delete themselves from a household, they should delete the household itself then.

#### Endpoints to edit the Catlaog Table

All endpoints are authorized for an authenticated member( owner or member- both are allowed) of household.
1. POST /households/{household-id}/catalog
Create a new item in catalog.
2. GET /households/{household-id}/catalog/all
Get all items in household catalog.
3. GET /households/{household-id}/catalog/{item-id}
Get a specific item in household catalog.
4. PATCH /households/{household-id}/catalog/{item-id}
Update the details of a specific item
5. DELETE /households/{household-id}/catalog/{item-id}
Delete the item from the catalog. Delete if item in inventory
or shopping list. 

#### Endpoints to edit the Inventory Table

All endpoints are authorized for authenticated member(owner / member) of household.
1. POST /households/{household-id}/inventory
Add a new item to the inventory. Add details in payload. Enforce constraint of no batch duplicates. Send error
409 conflict.
2. GET /households/{household-id}/inventory/all
Get all the items in the inventory of a household.
3. GET /households/{household-id}/catalog/{item_id}/inventory
Get the details of a specific item in inventory using the item's unique id (catalog based). Should return all instances of item
in inventory.
4. PATCH /households/{household-id}/inventory/{inventory_id}
Update the qty from the inventory.

NOTE: A decision needs to be made about future items tracking. 
If a person purchases an item when stock already remains, how
do we add it to inventory ? Do we create a new inventory item
or do we use the same inventory item, and update the qty,
what about the expiries ? E.g milk

Solution ideas:
- Have a separate inventory entry for the new product. Uniqueness
constraint will then inlcude expiry, household, item.


5. DELETE /households/{household-id}/inventory/{inventory_id}
Delete the item from inventory. Missing item returns 404.

### Endpoints to edit the Cart

All endpoints are authorized for authenticated member(owner / member) of household.
1. POST /households/{household-id}/cart
Add a new item to the shopping cart. Add details in payload. Enforce constraint of no duplicates. 
Send error 409 conflict.
2. GET /households/{household-id}/cart
Get all the items in the cart.
3. GET /households/{household-id}/cart/{item-id}
Get detials of a specific item in cart.
4. PATCH /households/{household-id}/cart/{item-id}
Update the item details such as qty, is_bought in the cart.
5. DELETE /households/{household-id}/cart/{item-id}
Remove the item from the shopping cart.
6. DELETE /households/{household-id}/cart
Clear the entire shopping cart.


### Frontend Principles

Mobile development is the primary focus for this project. Each screen should have a valid main action flow,
empty state flow, error state flow.

### Key Frontend Decisions

Core screens to develop
1. Login/Signup page
2. Login page
3. Signup page
4. Households List
5. Individual Household Page
6. Inventory
7. Cart


General features of app
- All screen will have a wallpaper of grocery items in light
- All text will be Calibri, size 11
- All test boxes will be rounded


### Implementation Order for frontend
1. App foundations
2. Auth flow
3. Household Selection
4. Inventory read first, then write
5. Cart read first, then write

User flow for using the app
1. First login / signup
2. On Sign in, a page with household list shows up.
3. On clicking a particular household page shows up.
4. From household page, user has access to that household's inventory and cart pages.




For dev purposes use the user
username: testuser1
password: TestPass123!



