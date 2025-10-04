fun main() {
    //People stored in file
    val peopleFile = "data/people.json"
    //Load people to list
    val people = JsonUtils.loadPeopleFromFile(peopleFile).toMutableList()

    //Ensure that the list isn't empty
    println("Loaded ${people.size} participants.")

    //Allow user to add participants if needed
    print("Do you want to add any new participants? (y/n): ")
    if (readLine()?.lowercase() == "y") {
        while (true) {
            print("Enter name (or blank to finish): ")
            val name = readLine()?.trim().orEmpty()
            if (name.isBlank()) break

            print("Enter family ID for $name: ")
            val familyId = readLine()?.trim().orEmpty()

            print("Is $name a kid? (y/n): ")
            val isKid = readLine()?.trim()?.lowercase() == "y"

            val newPerson = Person(name, familyId, isKid)
            people.add(newPerson)
            println("Added: $newPerson")
        }

        JsonUtils.savePeopleToFile(people, peopleFile)
        println("Updated people list saved to $peopleFile")
    }

    // New: allow user to remove people
    promptRemovePeople(people)

    // Load last year's assignments as forbidden (one-way giver→recipient)
    val forbidden = JsonUtils.loadAssignmentsFromFile("data/assignments_2024.json")

    // Generate new assignments
    val pairings = generatePairings(people, forbidden)

    // Print and save results
    println("\nGift Exchange Assignments:")
    pairings.forEach { (giver, recipient) ->
        println(" - ${giver.name} ➝ ${recipient.name}")
    }

    println("Pairings size: ${pairings.size}")
    JsonUtils.saveAssignmentsToFile(pairings, "data/assignments_2025.json")
}

//Function to remove people from the list if desired. Also allow to remove families
fun promptRemovePeople(people: MutableList<Person>) {
    while (true) {
        println("\nCurrent participants:")
        people.forEach { person ->
            println(" - ${person.name} (${if (person.isKid) "Kid" else "Adult"}, Family: ${person.familyId})")
        }

        print("Do you want to remove anyone? (y/n): ")
        if (readLine()?.trim()?.lowercase() != "y") break

        print("Enter the name of the person to remove (or blank to cancel): ")
        val input = readLine()?.trim()
        if (input.isNullOrBlank()) break

        // Find matches (case-insensitive)
        val matches = people.filter { it.name.equals(input, ignoreCase = true) }

        when {
            matches.isEmpty() -> {
                println("No participant found with the name \"$input\". Please try again.")
            }
            matches.size == 1 -> {
                val toRemove = matches.first()
                print("Remove ${toRemove.name} (family: ${toRemove.familyId})? (y/n): ")
                if (readLine()?.trim()?.lowercase() == "y") {
                    // 🔑 Ask if we should remove the whole family
                    print("Also remove all members of family ${toRemove.familyId}? (y/n): ")
                    if (readLine()?.trim()?.lowercase() == "y") {
                        val familyMembers = people.filter { it.familyId == toRemove.familyId }
                        people.removeAll(familyMembers)
                        println("Removed entire family ${toRemove.familyId}: " +
                                familyMembers.joinToString { it.name })
                    } else {
                        people.remove(toRemove)
                        println("${toRemove.name} has been removed.")
                    }
                } else {
                    println("Removal cancelled.")
                }
            }
            else -> {
                // Multiple matches (same name) — list with families to clarify
                println("Multiple participants found with the name \"$input\":")
                matches.forEachIndexed { index, person ->
                    println("  [$index] ${person.name} (Family: ${person.familyId}, ${if (person.isKid) "Kid" else "Adult"})")
                }
                print("Enter the number of the person to remove (or blank to cancel): ")
                val selection = readLine()?.trim()
                val idx = selection?.toIntOrNull()
                if (idx != null && idx in matches.indices) {
                    val toRemove = matches[idx]
                    print("Remove ${toRemove.name} (family: ${toRemove.familyId})? (y/n): ")
                    if (readLine()?.trim()?.lowercase() == "y") {
                        // 🔑 Ask for whole family removal
                        print("Also remove all members of family ${toRemove.familyId}? (y/n): ")
                        if (readLine()?.trim()?.lowercase() == "y") {
                            val familyMembers = people.filter { it.familyId == toRemove.familyId }
                            people.removeAll(familyMembers)
                            println("Removed entire family ${toRemove.familyId}: " +
                                    familyMembers.joinToString { it.name })
                        } else {
                            people.remove(toRemove)
                            println("${toRemove.name} has been removed.")
                        }
                    } else {
                        println("Removal cancelled.")
                    }
                } else {
                    println("Invalid selection, cancellation assumed.")
                }
            }
        }
    }
}