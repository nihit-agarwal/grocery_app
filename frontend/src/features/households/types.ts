export type Household = {
    household_id: string;
    house_name: string;
    role: string;
    joined_at: string;
}

export type HouseholdListResponse = {
    households: Household[];
};