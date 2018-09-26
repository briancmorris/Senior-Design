import random as r

contact_id = "Brian"
action_types = ["account_created", "email_opened", "opened_website", "added_item_to_cart", "item_purchased"]
actions = []

for i in range(25):
    actions.append(contact_id)
    actions.append("" + str(r.randint(0, 1000)) + " UTC")
    if i == 0:
        actions.append(action_types[i])
    else:
        actions.append(action_types[r.randint(1, 4)])

idx = 0
for i in range(25):
    print(actions[idx], actions[idx+1], actions[idx+2])
    idx += 3
