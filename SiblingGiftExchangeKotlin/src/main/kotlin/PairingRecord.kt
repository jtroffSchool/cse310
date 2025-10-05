import kotlinx.serialization.Serializable

@Serializable
//Declaration of class for Pairing Records
data class PairingRecord(
    val giver: Person,
    val recipient: Person
)
