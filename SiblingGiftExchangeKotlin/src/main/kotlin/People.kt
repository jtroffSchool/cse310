import kotlinx.serialization.Serializable

@Serializable
//Declaration class of a person
data class Person(
    val name: String,
    val familyId: String,
    val isKid: Boolean
)