//Function to pair people given various restrictions
fun generatePairings(
    people: List<Person>,
    forbidden: Set<Pair<String, String>>
): Map<Person, Person> {
    val adults = people.filter { !it.isKid }
    val kids = people.filter { it.isKid }

    fun isValidPair(
        giver: Person,
        recipient: Person,
        currentPairs: Map<Person, Person>
    ): Boolean {
        // No self
        if (giver == recipient) return false

        // No same family
        if (giver.familyId == recipient.familyId) return false

        // Not forbidden (one-way)
        if (giver.name to recipient.name in forbidden) return false

        // No reciprocal person pairing (if recipient already assigned to give to this giver)
        if (currentPairs[recipient] == giver) return false

        return true
    }

    //Function to help check Adult Direction constraints
    fun checkAdultDirectionConstraints(pairs: Map<Person, Person>): Boolean {
        // Count how many times familyA -> familyB occurs
        val directionCount = mutableMapOf<Pair<String, String>, Int>()

        pairs.forEach { (giver, recipient) ->
            if (!giver.isKid && !recipient.isKid) {
                val key = giver.familyId to recipient.familyId
                directionCount[key] = directionCount.getOrDefault(key, 0) + 1
            }
        }

        // Enforce: at most one A -> B for every ordered family pair (A,B)
        if (directionCount.any { it.value > 1 }) return false

        // NOTE: we DO NOT forbid having both (A->B) and (B->A) at family level,
        // as long as each ordered pair appears at most once and person-level reciprocity
        // is prevented above in isValidPair.

        return true
    }

    // Deterministic backtracking solver for a group (adults or kids)
    fun backtrack(
        givers: List<Person>,
        receivers: MutableList<Person>,
        currentPairs: MutableMap<Person, Person>,
        adultsOnly: Boolean
    ): Boolean {
        if (givers.isEmpty()) {
            // Validate adult-only directional constraints at the end
            return !adultsOnly || checkAdultDirectionConstraints(currentPairs)
        }

        val giver = givers.first()
        // Heuristic: try receivers in random or deterministic order —
        // deterministic here keeps it repeatable; shuffle if you want variation.
        for (recipient in receivers.toList()) {
            if (!isValidPair(giver, recipient, currentPairs)) continue

            // Tentatively assign
            currentPairs[giver] = recipient
            receivers.remove(recipient)

            if (backtrack(givers.drop(1), receivers, currentPairs, adultsOnly)) {
                return true
            }

            // Undo and continue
            currentPairs.remove(giver)
            receivers.add(recipient)
        }
        return false
    }

    //Verify success of pairing
    fun solveGroup(group: List<Person>, adultsOnly: Boolean): Map<Person, Person> {
        if (group.size < 2) return emptyMap()
        val pairs = mutableMapOf<Person, Person>()
        val success = backtrack(group, group.toMutableList(), pairs, adultsOnly)
        if (!success) error("No valid solution for ${if (adultsOnly) "adults" else "kids"}")
        return pairs
    }

    val result = mutableMapOf<Person, Person>()
    result.putAll(solveGroup(adults, adultsOnly = true))
    result.putAll(solveGroup(kids, adultsOnly = false))
    return result
}
