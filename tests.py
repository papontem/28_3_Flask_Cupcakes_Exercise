from unittest import TestCase

from app import app
from models import db, Cupcake
import traceback

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    # Part Four: Write More Tests
    # Add tests for the PATCH and DELETE routes.
    def test_patch_cupcake(self):
        with app.test_client() as client:
            """ test that we are updating a desired cupcake with new data and that it is then reflected in our database"""

            # Prepare the data for the update request
            updated_cupcake_data = {
                "flavor": "UpdatedTestCupcakeFlavor",
                "size": "TestSize9000",
                "rating": 25,
                "image": "http://test.com/cupcake_test_image.jpg"
            }

            try:
                
                ## python debugger here to help ^.^ !
                # import pdb; pdb.set_trace()

                # Send a PATCH request to update the cupcake with self.cupcake.id
                resp = client.patch(f"/api/cupcakes/{self.cupcake.id}", json=updated_cupcake_data)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that our patch route for cupcakes api is working.")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                # Check if the response matches the updated data
                self.assertEqual( 
                    resp.json,
                    {
                        "cupcake": {
                        "id": self.cupcake.id, 
                        "flavor": "UpdatedTestCupcakeFlavor",
                        "size": "TestSize9000",
                        "rating": 25,
                        "image": "http://test.com/cupcake_test_image.jpg"
                        }
                    }
                )

                # Check if the cupcake was actually updated in the database
                cupcake = Cupcake.query.get(self.cupcake.id)
                self.assertEqual(cupcake.flavor, "UpdatedTestCupcakeFlavor")
                self.assertEqual(cupcake.size, "TestSize9000")
                self.assertEqual(cupcake.rating, 25)
                self.assertEqual(cupcake.image, "http://test.com/cupcake_test_image.jpg")


    def test_delete_cupcake(self):
        with app.test_client() as client:
            """
                test that when we delete a cupcake we get a sucess and a message saying deleted.
                TODO: test that the number of cupcakes in our database has decreased by 1.
                TODO: might be a different test, that if we try to delete a cupcake that downs exist that we get a 404
            """
            try:
                
                ## python debugger here to help ^.^ !
                # import pdb; pdb.set_trace()

                # Send a DELETE request to update the cupcake with self.cupcake.id
                resp = client.delete(f"/api/cupcakes/{self.cupcake.id}")

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that our delete route for cupcakes api is working.")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json, {"message": "Deleted"})
