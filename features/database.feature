Feature: Database custom declarative resource
    Scenario: Created database just with a name
        Given a running shell-operator
        When following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: Database
        metadata:
          name: hello
        """
        Then database "hello" exists

    Scenario: Created database is deleted
        Given a running shell-operator
        When following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: Database
        metadata:
          name: hello
        """
        But previous kubernetes configuration is deleted
        Then database "hello" does not exist
