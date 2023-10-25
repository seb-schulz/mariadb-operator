Feature: User custom declarative resource
    Scenario: Created user just with a name
        Given a running shell-operator
        When following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: User
        metadata:
          name: hello
        """
        Then user "hello" exists

    Scenario: Created user is deleted
        Given a running shell-operator
        When following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: User
        metadata:
          name: hello
        """
        But previous kubernetes configuration is deleted
        Then user "hello" does not exist


    Scenario: Config map does exist on configured namespace
        Given a running shell-operator
        When namespace "myapp" exists
        And following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: User
        metadata:
          name: hello
        spec:
          database: mydb
          configMaps:
            - namespace: myapp
              name: mycm
        """
        And following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: Database
        metadata:
          name: mydb
        """
        Then config map "mycm" does exist in namespace "myapp" with following entries
            | key                       | value                             |
            | MARIADB_SERVICE_DOMAIN    | mariadb.default.svc.cluster.local |
            | MARIADB_SERVICE_PORT      | 3306                              |
            | MARIADB_USER              | hello                             |


    Scenario: Secret does exist on configured namespace
        Given a running shell-operator
        When namespace "myapp2" exists
        And following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: Database
        metadata:
          name: mydb
        """
        And following kubernetes configuration is applied
        """
        apiVersion: "k8s.sebatec.eu/v1alpha1"
        kind: User
        metadata:
          name: hello
        spec:
          database: mydb
          secrets:
            - namespace: myapp2
              name: mysecret
        """
        Then secret "mysecret" does exist in namespace "myapp2" with following entries
            | key               |
            | MARIADB_PASSWORD  |
