import { Paper, 
    Stack, 
    Title, 
    Text,
    Button, 
    Group, 
    Loader,
    Alert,
    Card } from "@mantine/core";
import { useState, useContext, useEffect } from "react";
import { AuthContext } from "../auth/AuthContext";
import { http } from "../../services/http";
import { Link, useNavigate } from "react-router-dom";
import type { HouseholdListResponse, Household } from "./types";




export default function HouseholdListPage() {
    const {logout} = useContext(AuthContext);
    const [loggingOut, setLoggingOut] = useState(false);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [households, setHouseholds] = useState<Household[]>([]);
    const navigate = useNavigate();


    useEffect(() => {
        async function loadHouseholds() {
            try {
                setError("");
                const response = await http.get<HouseholdListResponse>("/members/me");
                setHouseholds(response.data.households);
            } catch {
                setError("Could not load your household right now")
            } finally {
                setLoading(false);
            }
        }
        loadHouseholds();
    }, [])

    async function handleLogout() {
        try {
            setLoggingOut(true);
            await logout();
        } finally {
            setLoggingOut(false);
        }
    }

    async function createHousehold() {
        try {
            navigate("/households/create", {replace: true});
        } catch {
            console.log("Cannot create new household")
        }
    }

    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Your households</Title>
                        <Text c="dimmed">
                            Select a household to open its workspace.
                        </Text>
                    </div>
                    <Button
                    variant="light"
                    color="gray"
                    onClick={handleLogout}
                    loading={loggingOut}
                    >Log Out </Button>

                    {loading ? (
                        <Group>
                            <Loader size="sm"/>
                            <Text c="dimmed">Loading households...</Text>
                        </Group>
                    ): null}

                    {error ? (
                        <Alert color="red" title="Could not load households">
                            {error}
                        </Alert>
                    ): null}

                    {!loading && !error && households.length === 0 ? (
                        <Card withBorder radius="lg" p="lg">
                            <Text c="dimmed" mt={4}>
                                Create one to start tracking inventory and shopping.
                            </Text>
                        </Card>
                    ): null}

                    <Stack gap="sm">
                        {households.map((household) => 
                        <Card
                        key={household.household_id}
                        withBorder
                        radius="lg"
                        p="md"
                        component={Link}
                        to={"/households/" + household.household_id}
                        state={{
                            hosueholdId: household.household_id,
                            houseName: household.house_name,
                            role: household.role,
                            joinedAt: household.joined_at,
                        }}
                        style={{ textDecoration: "none"}}
                        >
                            <Group justify="space-between" align="center">
                                <div>
                                    <Text fw={700}>{household.house_name}</Text>
                                    <Text size="sm" c="dimmed">
                                        Joined {new Date(household.joined_at).toLocaleDateString()}
                                    </Text>
                                </div>
                            </Group>


                        </Card>)}
                    </Stack>

                    <Button 
                    fullWidth
                    radius="xl"
                    variant="filled"
                    color="green"
                    onClick={createHousehold}>
                        Create new household
                    </Button>
                </Stack>
            </Paper>
        </main>
    )
}