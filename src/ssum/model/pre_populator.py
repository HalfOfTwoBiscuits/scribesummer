import json
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

from scribesummer.src.ssum.model.models import Category, SubscriptionPreset, SubscriptionPresetTier

class PrePopulator:
    '''Class responsible for pre-populating data from JSON.'''

    __db: SQLAlchemy
    __data_dir: Path

    def __init__(self, db: SQLAlchemy):
        self.__db = db
        self.__data_dir = Path("scribesummer/src/ssum/model/data").resolve()

    def populate(self):
        '''Load in JSON for subscription categories and presets.
        May raise FileNotFoundError, JSONDecodeError, UnicodeDecodeError, etc
        if data is absent or in an invalid format.
        
        If a category or preset already exists then it will be updated.'''

        # Load JSON.
        with open(self.__data_dir / "categories.json") as file:
            category_data = json.load(file)

        with open(self.__data_dir / "presets.json") as file:
            preset_data = json.load(file)
        
        # Create category objects.
        # Store them in a dict for reference when creating presets.
        categories = {}
        for cat_attrs_dict in category_data:
            category = Category(**cat_attrs_dict)
            categories[category.id] = category

            # Merge with the existing object.
            existing_category = self.__db.session.get(Category, category.id) 
            if existing_category:
                category = self.__db.session.merge(existing_category)
            
            self.__db.session.add(category)

        # Create preset objects.
        for preset_data_dict in preset_data:

            # Retrieve category objects.
            categories_for_preset = [
                categories[id]
                for id in preset_data_dict.pop("categories")
            ]

            # Create tier objects.
            tiers_for_preset = []
            for tier_data_dict in preset_data_dict.pop("tiers"):

                # Tiers have the preset's categories and
                # may optionally specify extra categories
                # for benefits specific to the tier.
                categories_for_tier = categories_for_preset.copy()
                try: 
                    categories_for_tier += tier_data_dict.pop("extra_categories")
                except KeyError: pass

                tier = SubscriptionPresetTier(**tier_data_dict)
                tiers_for_preset.append(tier)
            
            # Add tiers to preset.
            preset_data_dict['tiers'] = tiers_for_preset
            preset = SubscriptionPreset(**preset_data_dict)

            # Merge with the existing object.
            existing_preset = self.__db.session.get(SubscriptionPreset, preset.id)
            if existing_preset:
                preset = self.__db.session.merge(existing_preset)
            
            self.__db.session.add(preset)

        self.__db.session.commit()
        
        
