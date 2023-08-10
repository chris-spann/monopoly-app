# # from app.game import get_utility_rent


# from routers.gamespaces import get_utility_rent


# def test_get_utility_rent():
#     # Test case 1: Both utilities are owned by the same player
#     rent = get_utility_rent(owner_id=1, utility_id=12, roll_result=7)
#     assert rent.raw == 28
#     assert rent.multiplier == 10

#     # Test case 2: Both utilities are owned by different players
#     rent = get_utility_rent(utility1_owner_id=1, utility2_owner_id=2, roll_result=7)
#     assert rent.raw == 14
#     assert rent.multiplier == 4

#     # Test case 3: One utility is owned by the bank
#     rent = get_utility_rent(utility1_owner_id=None, utility2_owner_id=1, roll_result=7)
#     assert rent.raw == 14
#     assert rent.multiplier == 4

#     # Test case 4: Both utilities are owned by the bank
#     rent = get_utility_rent(utility1_owner_id=None, utility2_owner_id=None, roll_result=7)
#     assert rent.raw == 10
#     assert rent.multiplier == 4
