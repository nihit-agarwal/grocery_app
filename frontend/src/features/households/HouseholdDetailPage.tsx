import {
    ActionIcon,
    Alert,
    Button,
    Card,
    Group,
    Paper,
    Stack,
    Text,
    Title
} from "@mantine/core"
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { http } from "../../services/http";
import type { JSX } from "react/jsx-runtime";
import { IconArrowLeft } from "@tabler/icons-react";
import { useEffect, useMemo, useState } from "react";
import type { Household, HouseholdListResponse } from "./types";


function IsOwner({children, role} : {children: JSX.Element; role: string}) {
    return role === "owner" ? children : null;
}

export default function HouseholdDetailPage() {

    const { householdid } = useParams();
    const [error, setError] = useState("");
    const [households, setHouseholds] = useState<Household[]>([]);
    const [loading, setLoading] = useState(true);
    

    // Run GET method
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

    // Extract the household details
    const household = useMemo(() => households.find((household) => household.household_id === householdid), [households, householdid]);
    const navigate = useNavigate();

    async function deleteHousehold() {

        try {
            await http.delete(`/households/${householdid}`);
            navigate("/households", { replace: true})
        } catch {
            console.log("Error! Cannot delete household")
        }
    }

    const householdId = household?.household_id ?? householdid ?? "";
    const householdName = household?.house_name ?? "Household";
    const householdRole = household?.role ?? "member";
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <Group justify="space-between" align="center">
                        <ActionIcon
                        variant="light"
                        color="gray"
                        radius="xl"
                        aria-label="Back to household"
                        onClick={() => navigate(`/households`, {replace: true})}
                        >
                            <IconArrowLeft size={18} />
                        </ActionIcon>
                    </Group>
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> {householdName} </Title>
                        <Text c="dimmed">
                            Edit the inventory, cart, or catalog.
                        </Text>
                    </div>
                    
                    <IsOwner role={householdRole}>
                        <Stack gap="md" justify="flex-end" style={{ flexDirection: "row" }}>
                            <Button onClick={deleteHousehold} size="sm" radius="md" color="red">Delete</Button>    
                        </Stack>
                    </IsOwner>
                    
                    {error ? (
                        <Alert color="red" title="Could not load the household">
                            {error}
                        </Alert>
                    ): null}

                    <Stack gap="md">
                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        component={Link}
                        to={"/households/" + householdId + "/catalog"}
                        >
                            Catalog
                        </Card>

                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        component={Link}
                        to={"/households/" + householdId + "/inventory"}
                        >
                            Inventory
                        </Card>

                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        component={Link}
                        to={"/households/" + householdId + "/cart"}
                        >
                            Cart
                        </Card>


                    </Stack>

                </Stack>
            </Paper>
        </main>
    )
}