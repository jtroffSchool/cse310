import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.File

@kotlinx.serialization.Serializable
// Serialization so we can store and extract the results from json
data class LegacyRecord(val giver: String, val recipient: String)

object JsonUtils {
    private val json = Json { prettyPrint = true; ignoreUnknownKeys = true }

    //Save giver and recipient assignments to a file
    fun saveAssignmentsToFile(assignments: Map<Person, Person>, filePath: String) {
        val records = assignments.map { (giver, recipient) ->
            PairingRecord(giver = giver, recipient = recipient)
        }
        File(filePath).writeText(json.encodeToString(records))
    }

    //Load previous giver and recipient assignments
    fun loadAssignmentsFromFile(filePath: String): Set<Pair<String, String>> {
        val file = File(filePath)
        if (!file.exists()) return emptySet()
        val text = file.readText()

        return try {
            // New format: giver/recipient as full Person objects
            val records = json.decodeFromString<List<PairingRecord>>(text)
            records.map { it.giver.name to it.recipient.name }.toSet()
        } catch (e: Exception) {
            // Fallback: old format (giver/recipient strings only)
            val legacyRecords = json.decodeFromString<List<LegacyRecord>>(text)

            val peopleFile = File("data/people.json")
            val people = if (peopleFile.exists()) {
                json.decodeFromString<List<Person>>(peopleFile.readText()).associateBy { it.name }
            } else emptyMap()

            val upgraded = legacyRecords.mapNotNull { legacy ->
                val giver = people[legacy.giver]
                val recipient = people[legacy.recipient]
                if (giver != null && recipient != null) {
                    PairingRecord(giver = giver, recipient = recipient)
                } else {
                    println("⚠️ Skipping: could not find ${legacy.giver} or ${legacy.recipient} in people.json")
                    null
                }
            }

            File(filePath).writeText(json.encodeToString(upgraded))
            println("✅ Upgraded $filePath to new format (giver/recipient).")

            upgraded.map { it.giver.name to it.recipient.name }.toSet()
        }
    }

    //Helper function to check that file exists
    fun loadPeopleFromFile(filePath: String): List<Person> {
        val file = File(filePath)
        return if (file.exists()) {
            json.decodeFromString(file.readText())
        } else {
            emptyList()
        }
    }

    //Helper function to help save people to file
    fun savePeopleToFile(people: List<Person>, filePath: String) {
        File(filePath).writeText(json.encodeToString(people))
    }
}
