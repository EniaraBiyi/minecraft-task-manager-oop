#Formatting user input will happen at CLI terminal. All input is formatted with .strip().lower() there before a method is ever called
class Task:
    #constructor receives arguments and instantiates with corresponding attributes
    #No validation needed. Fully trusts Manager's validation since it knows all the tasks and collections
    def __init__(self, name: str, players: set, locations: set, category: str):
        self._name = name
        self._players = players.copy()
        self._locations = locations.copy()
        self._category = category
        self._status = False

    def __str__(self):
        return f"{self._name}"

    #set status as True
    def check(self):
        if self._status:
            pass
            #raise exception
        self._status = True

    #set status as False
    def uncheck(self):
        if not self._status:
            pass
            #raise exception
        self._status = False

    def details(self):
        return {"name": self._name, "players": self._players.copy(), "locations": self._locations.copy(), "category": self._category, "complete": self._status}

    # safely return current status
    @property
    def is_complete(self):
        return self._status

    @property
    def name(self):
        return self._name

    @property
    def players(self):
        return frozenset(self._players)

    @property
    def locations(self):
        return frozenset(self._locations)

    @property
    def category(self):
        return self._category


class Collection:
    #constructor will be instantiated three times for players, locations and categories
    #the three collection objects are instantiated from Manager's constructor (composition)
    def __init__(self, item_type: str, item_type_plural: str, protected_item: str = None):
        self._items = set()
        self.item_type = item_type
        self.item_type_plural = item_type_plural
        self._protected_item = protected_item
        if protected_item is not None:
            self._items.add(protected_item)

    #checks if item is saved in collection
    def __contains__(self, item: str):
        return item in self._items

    #add item to collection
    def add_item(self, item):
        if item not in self._items:
            self._items.add(item)
        else:
            pass
            #Exception raised to caller (to show arg was rejected addition)

    #checks if item can be safely removed from collection
    def _check_removable(self, item):
        if item == self._protected_item:
            pass
            #raise error to show that caller attempted to remove protected item
        if item not in self._items:
            pass
            #raise error to show caller attempted to remove an unsaved item

    #remove item from collection
    def _remove_item(self, item):
        self._items.remove(item)

    def remove_if_unused(self, name, in_use):
        self._check_removable(name)  #raises error if item (name) cannot be removed safely
        if in_use:
            pass
            #raise error to let caller know that item cannot be removed
        self._remove_item(name)

    #returns all saved items in collection
    def list_items(self):
        return sorted(self._items)

    #returns the subset of items that are not saved in the collection
    def unknown(self, items):
        return set(items) - self._items


class Manager:
    def __init__(self):
        self._tasks = {} #dictionary will keep track of task objects as values keyed by name
        self._session_players = Collection("player", "players")
        self._session_locations = Collection("location", "locations")
        self._session_categories = Collection("category", "categories", "default")
        #The three Collection objects are instantiated

    def add_task(self, name: str, players: set, locations: set, category: str):
        if name in self._tasks:
            pass
            #exception is raised, and no task is instantiated

        if self._session_players.unknown(players):
            pass
            #exception is raised, and no task is instantiated

        if self._session_locations.unknown(locations):
            pass
            #exception is raised, and no task is instantiated

        if category not in self._session_categories:
            pass
            # exception is raised, and no task is instantiated

        #task instantiation
        self._tasks[name] = Task(name, players, locations, category)

    def rem_task(self, name: str):
        if name not in self._tasks:
            pass
            #exception is raised, and no task is deleted

        del self._tasks[name]
        #corresponding task is deleted

    #return tasks according to status of completion
    def tasks_by_status(self, required_status: bool):
        matching_tasks = []

        for task_name, task in self._tasks.items():
            if task.is_complete == required_status:
                matching_tasks.append(task_name)

        return sorted(matching_tasks)

    def _get_task(self, name: str):
        if name not in self._tasks:
            pass
            #raised exception to show task was not found
        return self._tasks[name]

    def search_task(self, name: str):
        return self._get_task(name).details()

    def check_task(self, name: str):
        self._get_task(name).check()

    def uncheck_task(self, name: str):
        self._get_task(name).uncheck()

    #add
    def add_player(self, name: str):
        self._session_players.add_item(name)

    def add_location(self, name: str):
        self._session_locations.add_item(name)

    def add_category(self, name: str):
        self._session_categories.add_item(name)

    # list
    def list_players(self):
        return self._session_players.list_items()

    def list_locations(self):
        return self._session_locations.list_items()

    def list_categories(self):
        return self._session_categories.list_items()

    # remove
    def remove_player(self, name: str):
        in_use = any(name in task.players for task in self._tasks.values())
        self._session_players.remove_if_unused(name, in_use)

    def remove_location(self, name: str):
        in_use = any(name in task.locations for task in self._tasks.values())
        self._session_locations.remove_if_unused(name, in_use)

    def remove_category(self, name: str):
        in_use = any(name == task.category for task in self._tasks.values())
        self._session_categories.remove_if_unused(name, in_use)

    def all_tasks(self):
        return sorted(self._tasks)

    def allstatus(self):
        pass
        #no implementation yet