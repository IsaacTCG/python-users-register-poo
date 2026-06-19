import math
import os
import subprocess
import time

try:
  import readline
except ImportError:
  readline = None

EMPTY_USER_FORM = {
  'name': '',
  'email': '',
  'age': '',
  'occupation': '',
}

users = {}

ITEMS_PER_PAGE = 5
current_page = 1

def clear_console():
  command = 'cls' if os.name == 'nt' else 'clear'
  subprocess.run(command, shell = True)

def total_pages():
  if not users:
    return 1

  return math.ceil(len(users) / ITEMS_PER_PAGE)

def go_to_previous_page():
  global current_page

  if current_page > 1:
    current_page -= 1
    
def go_to_next_page():
  global current_page

  if current_page < total_pages():
    current_page += 1

def go_to_last_page():
  global current_page
  current_page = total_pages()

def has_previous_page():
  return current_page > 1

def has_next_page():
  return current_page < total_pages()

def get_next_new_user_id():
  if not users:
    return 1
  
  return max(users.keys()) + 1

exist_readline_in_globals = globals().get('readline') is not None

def value_insert_hook(value = None):
  if value and exist_readline_in_globals:
    readline.insert_text(str(value))
    readline.redisplay()

def set_pre_input_hook(value = None):
  if exist_readline_in_globals:
    readline.set_pre_input_hook(lambda: value_insert_hook(value))

def clear_pre_input_hook():
  if exist_readline_in_globals:
    readline.set_pre_input_hook(None) 

def read_name(value = None):
  old_value = value
  set_pre_input_hook(old_value)

  try:
    while True:
      prompt_text = f"Name [{old_value}]: " if old_value else "Name: "
      value = input(prompt_text).strip().upper()

      clear_console()

      if not value and old_value:
        return old_value
      
      if not value:
        print("Name can't be blank.")
        continue
      
      if not value.replace(" ", "").isalpha():
        print("Name can't receive numbers.")
        continue

      return value

  finally:
    clear_pre_input_hook()

def email_exists(value, ignored_user_id = None):
  for user in users.values():
    if user.get('email') == value and user.get('id') != ignored_user_id:
      return True
    
  return False

def is_valid_email(value):
    if "@" not in value:
      return False

    local, domain = value.split("@", 1)

    if not local or not domain:
      return False

    if "." not in domain:
      return False

    return True
    
def read_email(value = None, user_id = None):
  old_value = value
  set_pre_input_hook(old_value)

  try:
    while True:
      prompt_text = f"Email [{old_value}]: " if old_value else "Email: "
      value = input(prompt_text).strip().upper()

      clear_console()

      if not value and old_value:
        return old_value

      if not value:
        print("Email can't be blank.")
        continue

      if not is_valid_email(value):
        print("Email invalid.")
        continue

      if email_exists(value, user_id):
        print("Email already exists.")
        continue

      return value
  
  finally:
    clear_pre_input_hook()
  
def read_age(value = None):
  old_value = value
  set_pre_input_hook(old_value)

  try:
    while True:
      prompt_text = f"Age [{old_value}]: " if old_value else "Age: "
      value = input(prompt_text).strip()

      clear_console()

      if not value and old_value:
        return old_value

      if not value:
        print("Age can't be blank.")
        continue

      try:
        value = int(value)
      except ValueError:
        print("Age can't receive characters. Must be a valid number.")
        continue

      if not value >= 0:
        print("Age must be more or equal than 0.")
        continue

      return value

  finally:
    clear_pre_input_hook()
  
def read_occupation(value = None):
  old_value = value
  set_pre_input_hook(old_value)

  try:
    while True:
      prompt_text = f"Occupation [{old_value}]: " if old_value else "Occupation: "
      value = input(prompt_text).strip().upper()

      clear_console()

      if not value and old_value:
        return old_value

      if not value:
        value = 'UNKNOWN'

      return value

  finally:
    clear_pre_input_hook()

def get_user_prototype(user):
  return {
    'name': read_name(user.get('name')),
    'email': read_email(user.get('email'), user.get('id')),
    'age': read_age(user.get('age')),
    'occupation': read_occupation(user.get('occupation'))
  }

def invalid_option_error():
  clear_console()
  print("The number insertted isn't a valid number.")
  print("")

def save_menu(title, user):
  clear_console()
  title()
  show_user(user)
  print("")
  print("1: Save")
  print("2: Cancel")

new_user_title = lambda: print("\n----- New User -----")

def create_user():
  new_user_title()

  new_user_id = get_next_new_user_id()
  user = get_user_prototype(EMPTY_USER_FORM)
  user['id'] = new_user_id

  save_menu(new_user_title, user)

  while True:
    try:
      print("")
      option = int(input('Insert an option: '))

      clear_console()

      match option:
        case 1:
          users[new_user_id] = user
          go_to_last_page()
          clear_console()
          break
        case 2:
          break
        case _:
          invalid_option_error()

    
    except ValueError:
      invalid_option_error()

  return

update_user_title = lambda: print("\n----- Update User -----")

def confirm_menu(title, operation, user):
  title()
  print(f"Are you sure you want to {operation} this user: {user.get('id')} - {user.get('name')}?")
  print("")
  print("1: Confirm")
  print("2: Cancel")

def update_user(user):
  updating_state = True

  while updating_state:
    confirm_menu(update_user_title, 'update', user)

    try:
      print("")
      option = int(input('Insert an option: '))

      clear_console()

      match option:
        case 1:
          update_user_title()
          updated_user = get_user_prototype(user)
          updated_user['id'] = user.get('id')

          save_menu(update_user_title, updated_user)

          saving_state = True

          while saving_state:
            try:
              print("")
              option = int(input('Insert an option: '))

              clear_console()

              match option:
                case 1:
                  users[user.get('id')] = updated_user
                  saving_state = False
                  updating_state = False

              saving_state = False
            
            except ValueError:
              invalid_option_error()
        case 2:
          updating_state = False
        case _:
          invalid_option_error()

    except ValueError:
      invalid_option_error()

delete_user_title = lambda: print("\n----- Delete User -----")

def delete_user(user):
  while True:
    confirm_menu(delete_user_title, 'delete', user)

    try:
      print("")
      option = int(input('Insert an option: '))

      clear_console()

      match option:
        case 1:
          users.pop(user.get('id'), None)
          go_to_previous_page() if current_page > total_pages() else None
          return True
        case 2:
          break
        case _:
          invalid_option_error()

    except ValueError:
      invalid_option_error()

find_user_title = lambda: print("\n----- Find User ------")
user_title = lambda id: print(f"\n----- User {id} ------")

def user_not_found_menu(user_id):
  while True:
    clear_console()
    find_user_title()
    print(f"User with ID {user_id} not found.")
    print('1: User list')
    print('2: Try again')

    try:
      print("")
      option = int(input("Insert an option: "))

      clear_console()

      match option:
        case 1:
          return False
        case 2:
          return True

    except ValueError:
      invalid_option_error()

def show_user(user):
  print(f"ID:         {user['id']}")
  print(f"NAME:       {user['name']}")
  print(f"EMAIL:      {user['email']}")
  print(f"AGE:        {user['age']}")
  print(f"OCCUPATION: {user['occupation']}")

def find_user(user_id = None):
  while True:
    find_user_title()

    try:
      if not user_id:
        user_id = int(input('Insert the user ID to find: '))

      user = users.get(user_id)

      if not user:
        try_again = user_not_found_menu(user_id)
          
        if not try_again:
          break

        user_id = None
        clear_console()
        continue
        
      else:
        clear_console()
        user_title(user_id)
        show_user(user)
        print("")
        print("1: User list")
        print("2: Update")
        print("3: Delete")

        try:
          print("")
          option = int(input('Insert an option: '))
          clear_console()

          match option:
            case 1:
              break
            case 2:
              clear_console()
              update_user(user)
            case 3:
              clear_console()
              if delete_user(user):
                break
            case _:
              invalid_option_error()

        except ValueError:
          invalid_option_error()

    except ValueError:
      clear_console()
      print("User ID must be a valid number.")
      print("")

def show_users_list():
  if len(users) == 0:
    print("The users list is empty.")
  else:
    print('ID  | NAME')
    for user in list(users.values())[(current_page - 1) * ITEMS_PER_PAGE : current_page * ITEMS_PER_PAGE]:
      print(f"{user.get('id'):<4}| {user.get('name')}")

def options_menu():
  print("1: Main Menu")
  print("2: Create")
  
  if users:
    print("3: Find")
  
  if len(users) > ITEMS_PER_PAGE:
    if has_previous_page():
      print("4: Back Page")
    
    if has_next_page():
      print("5: Next Page")

def show_list():
  while True:
    print("\n----- User list -----")
    show_users_list()
    print("")

    options_menu()

    try:
      print("")
      option = int(input("Insert an option: "))

      clear_console()

      match option:
        case 1:
          break
        case 2:
          clear_console()
          create_user()
        case 3:
          if users:
            clear_console()
            find_user()
        case 4:
          if users:
            go_to_previous_page()
        case 5:
          if users:
            go_to_next_page()
        case _:
          invalid_option_error()

    except ValueError:
      invalid_option_error()

def show_menu():
  while True:
    clear_console()
    print("\n----- Main Menu -----")
    print("1: Exit")
    print("2: List")
    
    try:
      print("")
      option = int(input("Insert an option: "))

      match option:
        case 1:
          clear_console()
          break
        case 2:
          clear_console()
          show_list()
        case _:
          invalid_option_error()

    except ValueError:
      invalid_option_error()

def main():
  show_menu()
  print("Exiting...")
  time.sleep(1)

if __name__ == "__main__":
  main()