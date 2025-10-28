from typing import Set, Dict
from dataclasses import dataclass

@dataclass
class CardValue:
    """Represents a detected card"""
    rank: str
    suit: str
    confidence: float

class CountingService:
    """Manages Hi-Lo card counting state"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.running_count = 0
            cls._instance.detected_cards: Set[str] = set()
        return cls._instance

    def get_card_value(self, rank: str) -> int:
        """
        Get Hi-Lo value for a card rank
        2-6: +1
        7-9: 0
        10-A: -1
        """
        high_cards = {'10', 'J', 'Q', 'K', 'A'}
        low_cards = {'2', '3', '4', '5', '6'}

        if rank in low_cards:
            return 1
        elif rank in high_cards:
            return -1
        else:
            return 0

    def process_card(self, card_id: str, rank: str) -> Dict:
        """
        Process a detected card and update count
        Returns dict with count change and new total
        """
        if card_id in self.detected_cards:
            # Card already counted
            return {
                "new_card": False,
                "count_change": 0,
                "running_count": self.running_count
            }

        # New card detected
        self.detected_cards.add(card_id)
        count_change = self.get_card_value(rank)
        self.running_count += count_change

        return {
            "new_card": True,
            "count_change": count_change,
            "running_count": self.running_count
        }

    def reset(self):
        """Reset count and detected cards"""
        self.running_count = 0
        self.detected_cards.clear()
        return {"running_count": 0, "detected_cards": 0}

    def get_state(self) -> Dict:
        """Get current counting state"""
        return {
            "running_count": self.running_count,
            "total_cards_detected": len(self.detected_cards)
        }

# Create singleton instance
counting_service = CountingService()
