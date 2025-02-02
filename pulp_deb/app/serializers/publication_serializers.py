from rest_framework.serializers import BooleanField, ValidationError
from pulpcore.plugin.serializers import (
    PublicationDistributionSerializer,
    PublicationSerializer,
)

from pulp_deb.app.models import DebDistribution, DebPublication, VerbatimPublication


class VerbatimPublicationSerializer(PublicationSerializer):
    """
    A Serializer for VerbatimPublication.
    """

    class Meta:
        fields = PublicationSerializer.Meta.fields
        model = VerbatimPublication


class DebPublicationSerializer(PublicationSerializer):
    """
    A Serializer for DebPublication.
    """

    simple = BooleanField(
        help_text="Activate simple publishing mode (all packages in one release component).",
        default=False,
    )
    structured = BooleanField(
        help_text="Activate structured publishing mode.", default=False
    )

    def validate(self, data):
        """
        Check that the publishing modes are compatible.
        """
        data = super().validate(data)
        if not data["simple"] and not data["structured"]:
            raise ValidationError(
                "one of simple or structured publishing mode must be selected"
            )
        return data

    class Meta:
        fields = PublicationSerializer.Meta.fields + ("simple", "structured")
        model = DebPublication


class DebDistributionSerializer(PublicationDistributionSerializer):
    """
    Serializer for DebDistributions.
    """

    class Meta:
        fields = PublicationDistributionSerializer.Meta.fields
        model = DebDistribution
